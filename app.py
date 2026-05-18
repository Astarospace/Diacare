from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()
load_dotenv(dotenv_path='secret.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)

GENDER_MALE = 1
GENDER_FEMALE = 2

SCHEDULE_AVAILABLE = 1
SCHEDULE_BUSY = 2

APPOINTMENT_PENDING = 1
APPOINTMENT_ACCEPTED = 2
APPOINTMENT_REJECTED = 3
APPOINTMENT_COMPLETED = 4


class Patients(db.Model):
    __tablename__ = 'Patients'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FullName = db.Column(db.String(120), nullable=False)
    PhoneNumber = db.Column(db.String(20), nullable=False)
    PasswordHash = db.Column(db.String(255), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Gender = db.Column(db.Integer, nullable=False)


class Doctors(db.Model):
    __tablename__ = 'Doctors'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FullName = db.Column(db.String(120), nullable=False)
    PhoneNumber = db.Column(db.String(20), nullable=False)
    PasswordHash = db.Column(db.String(255), nullable=False)
    Specialty = db.Column(db.String(80), nullable=False, default='Diabetes Specialist')
    RatingSum = db.Column(db.Integer, nullable=False, default=0)
    RatingCount = db.Column(db.Integer, nullable=False, default=0)
    ImagePath = db.Column(db.String(255), default='/images/doctor-placeholder.svg')


class Schedules(db.Model):
    __tablename__ = 'Schedules'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DoctorId = db.Column(db.Integer, db.ForeignKey('Doctors.Id', ondelete='CASCADE'), nullable=False)
    Hours = db.Column(db.String(80), nullable=False)
    Status = db.Column(db.Integer, nullable=False, default=SCHEDULE_AVAILABLE)
    doctor = db.relationship('Doctors', backref='schedules', foreign_keys=[DoctorId])


class Appointments(db.Model):
    __tablename__ = 'Appointments'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PatientId = db.Column(db.Integer, db.ForeignKey('Patients.Id', ondelete='CASCADE'), nullable=False)
    DoctorId = db.Column(db.Integer, db.ForeignKey('Doctors.Id', ondelete='CASCADE'), nullable=False)
    ScheduleId = db.Column(db.Integer, db.ForeignKey('Schedules.Id', ondelete='CASCADE'), nullable=False)
    Status = db.Column(db.Integer, nullable=False, default=APPOINTMENT_PENDING)
    patient = db.relationship('Patients', backref='appointments', foreign_keys=[PatientId])
    doctor = db.relationship('Doctors', backref='appointments', foreign_keys=[DoctorId])
    schedule = db.relationship('Schedules', backref='appointment', uselist=False, foreign_keys=[ScheduleId])


class AdminUsers(db.Model):
    __tablename__ = 'AdminUsers'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FullName = db.Column(db.String(120), nullable=False)
    PhoneNumber = db.Column(db.String(20), nullable=False)
    PasswordHash = db.Column(db.String(255), nullable=False)


class DoctorReviews(db.Model):
    __tablename__ = 'DoctorReviews'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DoctorId = db.Column(db.Integer, db.ForeignKey('Doctors.Id', ondelete='CASCADE'), nullable=False)
    PatientId = db.Column(db.Integer, db.ForeignKey('Patients.Id', ondelete='CASCADE'), nullable=False)
    Rating = db.Column(db.Integer, nullable=False)
    Comment = db.Column(db.String(1000), default='')
    CreatedAt = db.Column(db.DateTime, default=datetime.now)
    doctor = db.relationship('Doctors', backref='reviews', foreign_keys=[DoctorId])
    patient = db.relationship('Patients', backref='doctor_reviews', foreign_keys=[PatientId])


def gender_name(g):
    return 'Male' if g == GENDER_MALE else 'Female'


def appointment_status_name(s):
    m = {APPOINTMENT_PENDING: 'Pending', APPOINTMENT_ACCEPTED: 'Accepted',
         APPOINTMENT_REJECTED: 'Rejected', APPOINTMENT_COMPLETED: 'Completed'}
    return m.get(s, 'Unknown')


def enum(*values):
    return values


app.jinja_env.globals.update(zip=zip, gender_name=gender_name,
                             appointment_status_name=appointment_status_name,
                             GENDER_MALE=GENDER_MALE, GENDER_FEMALE=GENDER_FEMALE,
                             APPOINTMENT_PENDING=APPOINTMENT_PENDING,
                             APPOINTMENT_ACCEPTED=APPOINTMENT_ACCEPTED,
                             APPOINTMENT_REJECTED=APPOINTMENT_REJECTED,
                             APPOINTMENT_COMPLETED=APPOINTMENT_COMPLETED,
                             SCHEDULE_AVAILABLE=SCHEDULE_AVAILABLE, SCHEDULE_BUSY=SCHEDULE_BUSY,
                             enum=enum)


@app.context_processor
def inject_user():
    return dict(session=session)


# ───────────────────────── Default Controller ─────────────────────────

@app.route('/')
def index():
    return render_template('index.html', title='Home Page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('PhoneNumber', '').strip()
        password = request.form.get('Password', '')
        user_type = request.form.get('UserType', 'Patient')

        user = None
        if user_type == 'Patient':
            user = Patients.query.filter_by(PhoneNumber=phone, PasswordHash=password).first()
        elif user_type == 'Doctor':
            user = Doctors.query.filter_by(PhoneNumber=phone, PasswordHash=password).first()
        elif user_type == 'Admin':
            user = AdminUsers.query.filter_by(PhoneNumber=phone, PasswordHash=password).first()

        if user:
            session['user_id'] = user.Id
            session['user_name'] = user.FullName
            session['user_role'] = user_type
            if user_type == 'Patient':
                return redirect(url_for('index'))
            elif user_type == 'Doctor':
                return redirect(url_for('doctor_index'))
            elif user_type == 'Admin':
                return redirect(url_for('admin_index'))
        else:
            error = 'Invalid login attempt.'
            return render_template('login.html', title='Login', error=error)

    return render_template('login.html', title='Login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('FullName', '').strip()
        phone = request.form.get('PhoneNumber', '').strip()
        age = int(request.form.get('Age', 0))
        gender = int(request.form.get('Gender', GENDER_MALE))
        password = request.form.get('Password', '')

        existing = Patients.query.filter_by(PhoneNumber=phone).first()
        if existing:
            error = 'Phone number already registered.'
            return render_template('register.html', title='Register', error=error,
                                   full_name=full_name, phone=phone, age=age,
                                   gender=gender, password=password)

        patient = Patients(FullName=full_name, PhoneNumber=phone,
                           PasswordHash=password, Age=age, Gender=gender)
        db.session.add(patient)
        db.session.commit()
        flash('Account created successfully!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register')


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))


# ───────────────────────── Patient Controller ─────────────────────────

@app.route('/patient/book', methods=['GET'])
def patient_book():
    search_name = request.args.get('searchName', '').strip()
    specialty = request.args.get('specialty', '').strip()
    min_rating = request.args.get('minRating')
    min_rating = int(min_rating) if min_rating else None

    query = Doctors.query.join(Schedules).filter(
        Schedules.Status == SCHEDULE_AVAILABLE).distinct()

    if search_name:
        query = query.filter(Doctors.FullName.contains(search_name))
    if specialty:
        query = query.filter(Doctors.Specialty == specialty)

    doctors = query.all()

    doctor_cards = []
    for d in doctors:
        avg_rating = round(d.RatingSum / d.RatingCount, 1) if d.RatingCount > 0 else 0
        available_schedules = [s for s in d.schedules if s.Status == SCHEDULE_AVAILABLE]
        reviews = DoctorReviews.query.filter_by(DoctorId=d.Id).order_by(
            DoctorReviews.CreatedAt.desc()).all()
        doctor_cards.append({
            'doctor_id': d.Id,
            'full_name': d.FullName,
            'specialty': d.Specialty,
            'image_path': d.ImagePath,
            'average_rating': avg_rating,
            'available_schedules': available_schedules,
            'reviews': reviews
        })

    if min_rating is not None:
        doctor_cards = [dc for dc in doctor_cards if dc['average_rating'] >= min_rating]

    return render_template('patient/book.html', title='Book Appointment',
                           doctors=doctor_cards, search_name=search_name,
                           specialty=specialty, min_rating=min_rating)


@app.route('/patient/book-appointment', methods=['POST'])
def patient_book_appointment():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    schedule_id = request.form.get('scheduleId', type=int)
    schedule = Schedules.query.get(schedule_id)
    if not schedule or schedule.Status != SCHEDULE_AVAILABLE:
        flash('Please pick one of the available schedules.', 'error')
        return redirect(url_for('patient_book'))

    appointment = Appointments(PatientId=user_id, DoctorId=schedule.DoctorId,
                               ScheduleId=schedule.Id, Status=APPOINTMENT_PENDING)
    schedule.Status = SCHEDULE_BUSY
    db.session.add(appointment)
    db.session.commit()

    return redirect(url_for('patient_index'))


@app.route('/patient/leave-review', methods=['POST'])
def patient_leave_review():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    doctor_id = request.form.get('doctorId', type=int)
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment', '').strip()

    if rating is None or rating < 1 or rating > 5 or not comment:
        return redirect(url_for('patient_book'))

    review = DoctorReviews(DoctorId=doctor_id, PatientId=user_id,
                           Rating=rating, Comment=comment)
    doctor = Doctors.query.get(doctor_id)
    if doctor:
        doctor.RatingSum += rating
        doctor.RatingCount += 1

    db.session.add(review)
    db.session.commit()

    return redirect(url_for('patient_book'))


@app.route('/patient', methods=['GET'])
def patient_index():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    patient = Patients.query.get(user_id)
    if not patient:
        session.clear()
        return redirect(url_for('index'))

    appointments = Appointments.query.filter_by(PatientId=user_id).order_by(
        Appointments.Id.desc()).all()

    return render_template('patient/index.html', title='My Profile',
                           patient=patient, appointments=appointments, Gender=Patients.Gender)


@app.route('/patient/edit-info', methods=['POST'])
def patient_edit_info():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    patient = Patients.query.get(user_id)
    if patient:
        patient.FullName = request.form.get('fullName', patient.FullName)
        patient.PhoneNumber = request.form.get('phoneNumber', patient.PhoneNumber)
        patient.Age = int(request.form.get('age', patient.Age))
        patient.Gender = int(request.form.get('gender', patient.Gender))
        new_password = request.form.get('password', '').strip()
        if new_password:
            patient.PasswordHash = new_password
        db.session.commit()
        session['user_name'] = patient.FullName

    return redirect(url_for('patient_index'))


@app.route('/patient/cancel-appointment', methods=['POST'])
def patient_cancel_appointment():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    appointment_id = request.form.get('appointmentId', type=int)
    appointment = Appointments.query.filter_by(Id=appointment_id, PatientId=user_id).first()

    if appointment and appointment.Status == APPOINTMENT_PENDING:
        schedule = Schedules.query.get(appointment.ScheduleId)
        if schedule:
            schedule.Status = SCHEDULE_AVAILABLE
        db.session.delete(appointment)
        db.session.commit()

    return redirect(url_for('patient_index'))


# ───────────────────────── Doctor Controller ─────────────────────────

@app.route('/doctor', methods=['GET'])
def doctor_index():
    user_id = session.get('user_id')
    user_role = session.get('user_role')
    if not user_id or user_role != 'Doctor':
        return redirect(url_for('login'))

    doctor = Doctors.query.options(
        db.joinedload(Doctors.schedules),
        db.joinedload(Doctors.appointments).joinedload(Appointments.patient),
        db.joinedload(Doctors.appointments).joinedload(Appointments.schedule),
    ).filter_by(Id=user_id).first()

    if not doctor:
        session.clear()
        return redirect(url_for('index'))

    return render_template('doctor/index.html', title='Doctor Dashboard', doctor=doctor,
                           APPOINTMENT_PENDING=APPOINTMENT_PENDING,
                           APPOINTMENT_ACCEPTED=APPOINTMENT_ACCEPTED)


@app.route('/doctor/accept-appointment', methods=['POST'])
def doctor_accept_appointment():
    appointment_id = request.form.get('appointmentId', type=int)
    appt = Appointments.query.get(appointment_id)
    if appt and appt.Status == APPOINTMENT_PENDING:
        appt.Status = APPOINTMENT_ACCEPTED
        db.session.commit()
    return redirect(url_for('doctor_index'))


@app.route('/doctor/reject-appointment', methods=['POST'])
def doctor_reject_appointment():
    appointment_id = request.form.get('appointmentId', type=int)
    appt = Appointments.query.options(
        db.joinedload(Appointments.schedule)).get(appointment_id)
    if appt and appt.Status == APPOINTMENT_PENDING:
        appt.Status = APPOINTMENT_REJECTED
        if appt.schedule:
            appt.schedule.Status = SCHEDULE_AVAILABLE
        db.session.commit()
    return redirect(url_for('doctor_index'))


@app.route('/doctor/complete-appointment', methods=['POST'])
def doctor_complete_appointment():
    appointment_id = request.form.get('appointmentId', type=int)
    appt = Appointments.query.options(
        db.joinedload(Appointments.schedule)).get(appointment_id)
    if appt and appt.Status == APPOINTMENT_ACCEPTED:
        appt.Status = APPOINTMENT_COMPLETED
        if appt.schedule:
            appt.schedule.Status = SCHEDULE_AVAILABLE
        db.session.commit()
    return redirect(url_for('doctor_index'))


# ───────────────────────── Admin Controller ─────────────────────────

@app.route('/admin', methods=['GET'])
def admin_index():
    user_id = session.get('user_id')
    user_role = session.get('user_role')
    if not user_id or user_role != 'Admin':
        return redirect(url_for('login'))

    patients = Patients.query.all()
    doctors = Doctors.query.options(
        db.joinedload(Doctors.schedules),
        db.joinedload(Doctors.reviews),
    ).all()
    appointments = Appointments.query.options(
        db.joinedload(Appointments.patient),
        db.joinedload(Appointments.doctor),
        db.joinedload(Appointments.schedule),
    ).all()

    active_tab = request.args.get('tab', 'patients-tab')

    return render_template('admin/index.html', title='Admin Dashboard',
                           patients=patients, doctors=doctors, appointments=appointments,
                           active_tab=active_tab, Gender=Patients.Gender)


@app.route('/admin/update-patient', methods=['POST'])
def admin_update_patient():
    patient_id = request.form.get('Id', type=int)
    patient = Patients.query.get(patient_id)
    if patient:
        patient.FullName = request.form.get('FullName', patient.FullName)
        patient.PhoneNumber = request.form.get('PhoneNumber', patient.PhoneNumber)
        patient.PasswordHash = request.form.get('PasswordHash', patient.PasswordHash)
        patient.Age = int(request.form.get('Age', patient.Age))
        patient.Gender = int(request.form.get('Gender', patient.Gender))
        db.session.commit()
    tab = request.form.get('active_tab', 'patients-tab')
    return redirect(url_for('admin_index', tab=tab))


@app.route('/admin/delete-patient', methods=['POST'])
def admin_delete_patient():
    patient_id = request.form.get('id', type=int)
    patient = Patients.query.options(
        db.joinedload(Patients.doctor_reviews),
        db.joinedload(Patients.appointments).joinedload(Appointments.schedule),
    ).filter_by(Id=patient_id).first()
    if patient:
        for appt in patient.appointments:
            if appt.schedule:
                appt.schedule.Status = SCHEDULE_AVAILABLE
        DoctorReviews.query.filter_by(PatientId=patient_id).delete()
        Appointments.query.filter_by(PatientId=patient_id).delete()
        db.session.delete(patient)
        db.session.commit()
    tab = request.form.get('active_tab', 'patients-tab')
    return redirect(url_for('admin_index', tab=tab))


@app.route('/admin/update-doctor', methods=['POST'])
def admin_update_doctor():
    doctor_id = request.form.get('id', type=int)
    doctor = Doctors.query.options(db.joinedload(Doctors.schedules)).filter_by(Id=doctor_id).first()
    if doctor:
        doctor.FullName = request.form.get('fullName', doctor.FullName)
        doctor.PhoneNumber = request.form.get('phoneNumber', doctor.PhoneNumber)
        doctor.PasswordHash = request.form.get('passwordHash', doctor.PasswordHash)
        doctor.Specialty = request.form.get('specialty', doctor.Specialty)
        doctor.ImagePath = request.form.get('imagePath', doctor.ImagePath)

        schedule_hours = request.form.getlist('scheduleHours')
        schedules = sorted(doctor.schedules, key=lambda s: s.Id)
        for i, hours in enumerate(schedule_hours):
            if i < len(schedules):
                schedules[i].Hours = hours
        db.session.commit()
    tab = request.form.get('active_tab', 'doctors-tab')
    return redirect(url_for('admin_index', tab=tab))


@app.route('/admin/delete-doctor', methods=['POST'])
def admin_delete_doctor():
    doctor_id = request.form.get('id', type=int)
    doctor = Doctors.query.options(
        db.joinedload(Doctors.schedules),
        db.joinedload(Doctors.appointments),
        db.joinedload(Doctors.reviews),
    ).filter_by(Id=doctor_id).first()
    if doctor:
        DoctorReviews.query.filter_by(DoctorId=doctor_id).delete()
        Schedules.query.filter_by(DoctorId=doctor_id).delete()
        Appointments.query.filter_by(DoctorId=doctor_id).delete()
        db.session.delete(doctor)
        db.session.commit()
    tab = request.form.get('active_tab', 'doctors-tab')
    return redirect(url_for('admin_index', tab=tab))


@app.route('/admin/update-appointment', methods=['POST'])
def admin_update_appointment():
    appt_id = request.form.get('id', type=int)
    new_status = request.form.get('status', type=int)
    appt = Appointments.query.options(
        db.joinedload(Appointments.schedule)).get(appt_id)
    if appt:
        if appt.Status in (APPOINTMENT_REJECTED, APPOINTMENT_COMPLETED):
            tab = request.form.get('active_tab', 'appointments-tab')
            return redirect(url_for('admin_index', tab=tab))
        if new_status in (APPOINTMENT_REJECTED, APPOINTMENT_COMPLETED):
            if appt.schedule:
                appt.schedule.Status = SCHEDULE_AVAILABLE
        else:
            if appt.schedule:
                appt.schedule.Status = SCHEDULE_BUSY
        appt.Status = new_status
        db.session.commit()
    tab = request.form.get('active_tab', 'appointments-tab')
    return redirect(url_for('admin_index', tab=tab))


@app.route('/admin/delete-appointment', methods=['POST'])
def admin_delete_appointment():
    appt_id = request.form.get('id', type=int)
    appt = Appointments.query.options(
        db.joinedload(Appointments.schedule)).get(appt_id)
    if appt:
        if appt.schedule:
            appt.schedule.Status = SCHEDULE_AVAILABLE
        db.session.delete(appt)
        db.session.commit()
    tab = request.form.get('active_tab', 'appointments-tab')
    return redirect(url_for('admin_index', tab=tab))


@app.route('/admin/add-doctor', methods=['POST'])
def admin_add_doctor():
    doctor = Doctors(
        FullName=request.form.get('FullName', ''),
        PhoneNumber=request.form.get('PhoneNumber', ''),
        PasswordHash=request.form.get('PasswordHash') or 'Doctor@123',
        Specialty=request.form.get('Specialty', 'Diabetes Specialist'),
        ImagePath=request.form.get('ImagePath') or '/images/doctor-placeholder.svg',
    )
    db.session.add(doctor)
    db.session.flush()

    default_hours = ['04:00-06:00 | Saturday', '06:00-08:00 | Saturday', '08:00-10:00 | Saturday']
    for hours in default_hours:
        db.session.add(Schedules(DoctorId=doctor.Id, Hours=hours, Status=SCHEDULE_AVAILABLE))
    db.session.commit()

    return redirect(url_for('admin_index'))


@app.route('/error')
def error_page():
    return render_template('error.html', title='Error')


if __name__ == '__main__':
    app.run(debug=True, port=5220)
