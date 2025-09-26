from celery import shared_task
from django.utils import timezone
from datetime import date, datetime
from .models import Device, Employee, Attendance, AttendanceReport
import requests
from xml.etree import ElementTree as ET
import logging

logger = logging.getLogger(__name__)

@shared_task
def poll_attendance_devices():
    today = date.today()
    devices = Device.objects.all()
    
    for device in devices:
        try:
            if device.type == 'zk':
                # ZK Teco integration using pyzk
                try:
                    from pyzk import ZK, const
                    zk = ZK(device.serial_number, port=device.port or 4370, timeout=5, password=0, force_udp=False, ommit_pid=False)
                except ImportError:
                    logger.error("pyzk not available, skipping ZK device")
                    continue
                conn = zk.connect()
                att_logs = conn.get_attendance()
                
                for log in att_logs:
                    if log.timestamp.date() == today:
                        employee = Employee.objects.filter(device_id=str(log.user_id)).first()
                        if employee:
                            attendance, created = Attendance.objects.get_or_create(
                                department=employee.department,
                                date=today
                            )
                            AttendanceReport.objects.update_or_create(
                                employee=employee,
                                attendance=attendance,
                                defaults={'status': True}
                            )
                            logger.info(f"Updated attendance for {employee.admin.first_name} from ZK device {device.serial_number}")
                
                conn.disconnect()
                
            elif device.type == 'hik':
                # Hikvision integration using ISAPI
                start_time = today.strftime('%Y-%m-%dT00:00:00')
                end_time = today.strftime('%Y-%m-%dT23:59:59')
                url = f"http://{device.ip_address}:{device.port}/ISAPI/AccessControl/Attendance/GetAttendanceRecordList"
                params = {
                    'startTime': start_time,
                    'endTime': end_time,
                    'maxResults': 1000
                }
                auth = (device.username, device.password) if device.username else None
                
                response = requests.get(url, params=params, auth=auth, timeout=10)
                if response.status_code == 200:
                    root = ET.fromstring(response.content)
                    for record in root.findall('.//AttendanceRecord'):
                        employee_no = record.find('EmployeeNo').text
                        time_str = record.find('Time').text
                        if time_str:
                            log_time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')
                            if log_time.date() == today:
                                employee = Employee.objects.filter(device_id=employee_no).first()
                                if employee:
                                    attendance, created = Attendance.objects.get_or_create(
                                        department=employee.department,
                                        date=today
                                    )
                                    AttendanceReport.objects.update_or_create(
                                        employee=employee,
                                        attendance=attendance,
                                        defaults={'status': True}
                                    )
                                    logger.info(f"Updated attendance for {employee.admin.first_name} from Hikvision device {device.serial_number}")
                else:
                    logger.error(f"Hikvision API error for {device.serial_number}: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Error polling device {device.serial_number}: {str(e)}")
    
    logger.info("Attendance polling completed for all devices")
