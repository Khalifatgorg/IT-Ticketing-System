import os


mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
db = Session()
return db.query(User).get(int(user_id))


# Utility: send email (non-blocking would require background worker; here we'll keep it simple)
def send_email(subject, recipients, body):
try:
msg = Message(subject=subject, recipients=recipients, body=body)
mail.send(msg)
except Exception as e:
app.logger.warning('Mail send failed: %s' % e)


@app.route('/', methods=['GET','POST'])
def login():
db = Session()
form = LoginForm()
if form.validate_on_submit():
email = form.email.data.lower().strip()
user = db.query(User).filter_by(email=email).first()
if not user:
flash('No user with that email. Please ask Head to create your account.', 'warning')
return redirect(url_for('login'))
login_user(user)
flash('Logged in as %s' % user.name)
if user.role == 'head':
return redirect(url_for('dashboard_head'))
elif user.role == 'admin':
return redirect(url_for('dashboard_admin'))
else:
return redirect(url_for('dashboard_user'))
return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
logout_user()
return redirect(url_for('login'))


# HEAD dashboard
@app.route('/head', methods=['GET','POST'])
@login_required
def dashboard_head():
if current_user.role != 'head':
abort(403)
db = Session()
tickets = db.query(Ticket).order_by(Ticket.created_at.desc()).all()
admins = db.query(User).filter_by(role='admin').all()
form = NotifyForm()
if form.validate_on_submit():
note = Notification(content=form.content.data, created_by=current_user)
db.add(note)
db.commit()
# broadcast email
recipients = [u.email for u in db.query(User).filter(User.role.in_(['admin','user'])).all()]
send_email('Notification from Head', recipients, form.content.data)
flash('Notification posted and emailed', 'success')
return redirect(url_for('dashboard_head'))
return render_template('dashboard_head.html', tickets=tickets, admins=admins, form=form)


@app.route('/head/accept/<int:ticket_id>')
@login_required
def head_accept(ticket_id):
if current_user.role != 'head': abort(403)
db = Session()
t = db.query(Ticket).get(ticket_id)
if not t: abort(404)
t.status = 'Accepted-by-Head'
t.head_approved = True
t.history = (t.history or '') + f"\n{datetime.utcnow()}: Head {current_user.email} accepted ticket"
db.commit()
send_email('Your ticket accepted by Head', [t.created_by.email], f'Your ticket {t.id} has been accepted by Head.')
flash('Ticket accepted', 'success')
return redirect(url_for('dashboard_head'))


@app.route('/head/reject/<int:ticket_id>')
@login_required
def head_reject(ticket_id):
if current_user.role != 'head': abort(403)
db = Session()
t = db.query(Ticket).get(ticket_id)
if not t: abort(404)
t.status = 'Rejected'
t.head_approved = False
t.history = (t.history or '') + f"\n{datetime.utcnow()}: Head {current_user.email} rejected ticket"
db.commit()
send_email('Your ticket was rejected', [t.created_by.email], f'Your ticket {t.id} has been rejected by Head.')
flash('Ticket rejected', 'warning')
return redirect(url_for('dashboard_head'))


@app.route('/head/assign/<int:ticket_id>', methods=['POST'])
@login_required
def head_assign(ticket_id):
if current_user.role != 'head': abort(403)
admin_id = request.form.get('admin_id')
db = Session()
t = db.query(Ticket).get(ticket_id)
admin = db.query(User).get(int(admin_id)) if admin_id else None
if not t or not admin: abort(404)
t.assigned_admin = admin
t.status = 'Assigned'
t.history = (t.history or '') + f"\n{datetime.utcnow()}: Assigned to admin {admin.email} by Head"
db.commit()
send_e
