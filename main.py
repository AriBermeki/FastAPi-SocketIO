from adminui import (
    CombinedAction, 
    UpdateElement, 
    AdminApp, 
    BarChart, 
    Button, 
    Column, 
    Row, 
    LineChart, 
    Slider,
    TextField, 
    MenuItem, 
    FormActions, 
    TextArea, 
    SubmitButton,
    Form,
    
    )





app = AdminApp(use_fastapi=True)

def on_submit(form_data):
    print(form_data)

@app.page('/', 'main')
def form_page():
    return [
        Form(on_submit = on_submit, content = [
            TextField('Title'),
            TextArea('Description'),
            BarChart(),
            FormActions(content = [
                SubmitButton('Submit')
            ])
        ])
    ]


@app.page('/detail', 'main')
def form_page():
    return [
        
            TextField('Title'),
            TextArea('Description'),
            BarChart(),
            FormActions(content = [
                SubmitButton('Submit')
            ])
        
    ]
app.set_menu(
    [
        MenuItem('Form Page', '/', icon="dashboard"),
        MenuItem('Detail Page', '/detail', icon="info-circle")
    ]
)
server = app.prepare()




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=server)