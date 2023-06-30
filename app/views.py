from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Project

bp = Blueprint('views', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        project_description = request.form['description']
        if project_description:
            project = Project(description=project_description)
            db.session.add(project)
            db.session.commit()
            flash('Project added successfully!', 'success')
        else:
            flash('Description cannot be empty', 'danger')
        return redirect(url_for('views.index'))

    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@bp.route('/activate/<int:id>')
def activate(id):
    project = Project.query.get_or_404(id)
    project.status = 'active'
    db.session.commit()
    flash('Project activated', 'success')
    return redirect(url_for('views.index'))

@bp.route('/deactivate/<int:id>')
def deactivate(id):
    project = Project.query.get_or_404(id)
    project.status = 'inactive'
    db.session.commit()
    flash('Project deactivated', 'warning')
    return redirect(url_for('views.index'))

@bp.route('/delete/<int:id>')
def delete(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted', 'danger')
    return redirect(url_for('views.index'))
