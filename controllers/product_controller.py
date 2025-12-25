from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app.models.product import Product
from database import db

product_bp = Blueprint('product', __name__, url_prefix='/products')


@product_bp.route('/')
@login_required
def products():
    user_products = Product.query.filter_by(user_id=current_user.id).all()
    return render_template('products.html', products=user_products)


@product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        type = request.form['type']
        volume = float(request.form['volume'])
        strength = float(request.form['strength'])
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])

        new_product = Product(
            name=name,
            category=category,
            type=type,
            volume=volume,
            strength=strength,
            quantity=quantity,
            price=price,
            user_id=current_user.id
        )

        db.session.add(new_product)
        db.session.commit()

        flash('Продукт успешно добавлен!', 'success')
        return redirect(url_for('product.products'))

    return render_template('product_form.html', title='Добавить продукт')


@product_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)

    if product.user_id != current_user.id:
        flash('У вас нет прав для редактирования этого продукта', 'danger')
        return redirect(url_for('product.products'))

    if request.method == 'POST':
        product.name = request.form['name']
        product.category = request.form['category']
        product.type = request.form['type']
        product.volume = float(request.form['volume'])
        product.strength = float(request.form['strength'])
        product.quantity = int(request.form['quantity'])
        product.price = float(request.form['price'])

        db.session.commit()
        flash('Продукт успешно обновлен!', 'success')
        return redirect(url_for('product.products'))

    return render_template('product_form.html', title='Редактировать продукт', product=product)


@product_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)

    if product.user_id != current_user.id:
        flash('У вас нет прав для удаления этого продукта', 'danger')
        return redirect(url_for('product.products'))

    db.session.delete(product)
    db.session.commit()
    flash('Продукт успешно удален!', 'success')
    return redirect(url_for('product.products'))