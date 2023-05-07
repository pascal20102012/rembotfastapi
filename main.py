from datetime import datetime
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status
from starlette.templating import Jinja2Templates

app = FastAPI()
app.secret_key = str(uuid4())
templates = Jinja2Templates(directory='templates')
reminders = []


@app.get('/', response_class=HTMLResponse)
@app.post('/', response_class=HTMLResponse)
async def home(request: Request):
    if request.method == 'POST':
        form = await request.form()
        reminder_text = form['reminder']
        reminder_date = form['date']
        reminder_time = form['time']
        date_str = str(f'{reminder_date}{reminder_time}')
        date_obj = datetime.strftime(date_str, '%Y-%m-%d %H:%M')
        reminders.append(
            {
                'text': reminder_text,
                'date': date_obj
            }
        )
        return RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)
    now = datetime.now()
    upcoming_reminders = list()
    for index, reminder in enumerate(reminders):
        if reminder['time'] > now:
            reminder['index'] = index
            upcoming_reminders.append(reminder)
    return templates.TemplateResponse('home.html', {
        'request': request,
        'upcoming_reminders': upcoming_reminders
    })


@app.post('/delete/{index}')
async def remove_reminder(index: int):
    reminders.pop(index)
    return RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)


