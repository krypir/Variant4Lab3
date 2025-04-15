from flask import Flask, render_template, request
import requests

app = Flask(__name__)


def get_exchange_rate(base_currency, target_currency):
    try:
        response = requests.get(
            f"https://api.frankfurter.app/latest?from={base_currency}"
        )
        response.raise_for_status()
        data = response.json()
        return data['rates'].get(target_currency.upper())
    except Exception as e:
        print(f"Ошибка при получении курса: {e}")
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None

    if request.method == 'POST':
        # Получаем данные из формы
        amount_str = request.form.get('amount', '')
        from_curr = request.form.get('from_curr', '').upper()
        to_curr = request.form.get('to_curr', '').upper()

        # Валидация данных
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            error = "Введите корректную сумму (> 0)"
            return render_template('index.html', error=error, result=result)

        if not (from_curr and to_curr):
            error = "Выберите валюты"
            return render_template('index.html', error=error, result=result)

        # Получаем курс
        rate = get_exchange_rate(from_curr, to_curr)

        if rate is None:
            error = "Ошибка конвертации. Проверьте коды валют"
        else:
            result = {
                'amount': amount,
                'from_curr': from_curr,
                'to_curr': to_curr,
                'converted': round(amount * rate, 2)
            }

    return render_template('index.html', error=error, result=result)


if __name__ == '__main__':
    app.run(debug=True)
