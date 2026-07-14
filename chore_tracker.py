import flet as ft

#This block will be where any page configurations are stored.
def main(page: ft.Page):
    page.title = "Golly's Chores"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.width = 400
    page.height = 600
    page.bgcolor = ft.Colors.GREY_100
    
#This block will contain any global variables needed throughout the app.
    chore_column = ft.Column()
    current_active_chore = None
    current_active_row = None
    current_action = None
    total = float(0.00)
    total_paid = float(0.00)
    grand_chore_total = ft.Text(f"Total: $0.00", size=20, weight=ft.FontWeight.BOLD, expand=True)
    input_field = ft.TextField(label="Enter new Chore title:")
    input_field_2 = ft.TextField(label="Enter new Chore price:")
    input_field_3 = ft.TextField()

#This block creates the dialog box methods. These methods are used to set and open the various dialog boxes. The dialog boxes mimic a popout window.
    def show_edit_choices(e):
        nonlocal current_active_chore, current_active_row
        data_dict = e.control.data
        current_active_chore = data_dict["button"]
        current_active_row = data_dict["row"]
        page.show_dialog(edit_choice_dialog)
        page.update()

    def show_edit_confirm(e):
        nonlocal current_action
        if e.control.data == "Reset to Zero":
            current_action = "reset"
        elif e.control.data == "Delete":
            current_action = "delete"
        page.pop_dialog()
        page.show_dialog(edit_confirm_dialog)
        page.update()

    def show_button_edit(e):
        nonlocal current_active_chore
        page.pop_dialog()
        if current_active_chore and current_active_chore.data:
            input_field.value = current_active_chore.data["title"]
            input_field_2.value = str(current_active_chore.data["price"])
        page.show_dialog(edit_button_dialog)
        page.update()

    def action_handler_yes(e):
        nonlocal current_action
        if current_action == "reset":
            reset_button(e)
        elif current_action == "delete":
            delete_button(e)
        current_action=None
        page.pop_dialog()
        page.update()
    
    def show_pay_chore(e):
        nonlocal input_field_3
        page.show_dialog(pay_chore_dialog)
        page.update()


    
#This block creates the alert dialog boxes.
    edit_choice_dialog = ft.AlertDialog(
        modal = True,
        title = ft.Text("Edit Chore"),
        content = ft.Text("What do you want to do?"),
        actions=[
            ft.ElevatedButton("Reset to Zero", on_click=show_edit_confirm, data="Reset to Zero"),
            ft.ElevatedButton("Delete", on_click=show_edit_confirm, data="Delete"),
            ft.ElevatedButton("Edit title/price", on_click=show_button_edit),
        ],
    )

    edit_confirm_dialog = ft.AlertDialog(
        modal = True,
        title = ft.Text("Edit Chore"),
        content = ft.Text("Are you sure?"),
        actions=[
            ft.ElevatedButton("Yes", on_click=action_handler_yes),
            ft.ElevatedButton("No", on_click=lambda e: close_dialog(e)), 
        ],
    )

    edit_button_dialog = ft.AlertDialog(
        modal = True,
        title = ft.Text("Edit Chore"),
        content = ft.Column([input_field, input_field_2], tight=True),
        actions=[
            ft.ElevatedButton("Save", on_click=lambda e: edit_button(e))
        ],
    )

    pay_chore_dialog = ft.AlertDialog(
        modal=True,
        title = ft.Text("How much did you pay?!"),
        content = ft.Column([input_field_3], tight=True),
        actions=[
            ft.ElevatedButton("Save", on_click=lambda e: update_total_sub())
        ],
    )


#This is what allows the dialog boxes to display.
    page.overlay.extend([edit_choice_dialog, edit_button_dialog, edit_confirm_dialog, pay_chore_dialog])

#This block creates a method to create dynamic buttons and keep a running total.
    def show_input_view():
        main_view.visible = False
        input_view.visible = True
        page.update()
    
    
    def submit(e):
        title_text = new_chore_title.value
        price_text = float(new_chore_price.value)
        initial_data = {"title": title_text, "price": price_text, "sum": 0.00}            
        target_button = ft.ElevatedButton(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=300,
                controls=[
                    ft.Text(
                        f"{title_text}: ${price_text:.2f}",
                        size=17,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ORANGE_700
                    ), 
                    ft.Text(
                        f"${initial_data['sum']:.2f}",
                        size=15,
                        color=ft.Colors.ORANGE_700
                    )
                ]
            ),
        data = initial_data,
        on_click=button_click,
        )

        chore_row = ft.Row(
            controls=[
                target_button,
                ft.FloatingActionButton(
                    icon=ft.Icons.EDIT,
                    mini=True,
                    on_click=show_edit_choices,
                    data={"button": target_button, "row": None}
                )
            ],
            alignment=ft.MainAxisAlignment.START
        )
        chore_row.controls[1].data["row"] = chore_row
        new_chore_title.value = ""
        new_chore_price.value = ""
        chore_column.controls.append(chore_row)
        input_view.visible = False
        main_view.visible = True
        page.update()

#This block creates a method to reset the buttons sum back to $0.00.    
    def reset_button(e):
        nonlocal current_active_chore
        if current_active_chore and current_active_chore.data and "price" in current_active_chore.data:
            current_active_chore.data["sum"] = float(0.00)
            current_active_chore.content.controls[1].value =f"${current_active_chore.data['sum']:.2f}"
        current_active_chore = None
        update_total_add()


# This block edits the chore title and/or chore price.
    def edit_button(e):
        nonlocal current_active_chore
        if current_active_chore and current_active_chore.data:
            if input_field.value.strip():
                current_active_chore.data["title"] = input_field.value.strip()
            if input_field_2.value.strip():
                try:
                    current_active_chore.data["price"] = float(input_field_2.value.strip())
                except ValueError:
                    pass
            new_title = current_active_chore.data["title"]
            new_price = current_active_chore.data["price"]
            current_active_chore.content.controls[0].value =(f"{new_title}: ${new_price:.2f}")
        input_field.value = ""
        input_field_2.value = ""
        page.pop_dialog()
        update_total_add()
        current_active_chore = None
            

#This block creates a method to delete the button. 
    def delete_button(e):
        nonlocal current_active_row, current_active_chore
        if current_active_row and current_active_chore and chore_column.controls:
            if current_active_chore in chore_column.controls:
                chore_column.controls.remove(current_active_chore)
            if current_active_row in chore_column.controls:
                chore_column.controls.remove(current_active_row)
        current_active_row = None    
        current_active_chore = None  
        update_total_add()


#This block creates a method to increase the button's sum by the price of the chore.
    def button_click(e):
        button = e.control
        if button.data and "price" in button.data:
            button.data["sum"] += button.data["price"]
            button.content.controls[1].value =f"${button.data['sum']:.2f}"
            update_total_add()
            page.update()

#this ensures a clean closing of the dialog boxes.
    def close_dialog(e):
        page.pop_dialog()
        page.show_dialog(edit_choice_dialog)
        page.update()

#This keeps a running total of the buttons everytime one is created, the button is clicked, the button is reset, and the button is deleted.
    def update_total_add():
        nonlocal total, total_paid
        total = total_paid
        for control in chore_column.controls:
            if isinstance(control, ft.ElevatedButton) and control.data:
                total += control.data.get("sum", 0.0)
        grand_chore_total.value = f"Total: ${total:.2f}"
        page.update()

#This block reduces the total by $20
    def update_total_sub():
        nonlocal input_field_3, total_paid, total
        total_paid = total
        total_paid -= float(input_field_3.value) if input_field_3.value else 0.00
        input_field_3.value = ""
        reset_button_all()

    def reset_button_all():
        for buttons in chore_column.controls:
            if isinstance(buttons, ft.ElevatedButton) and buttons.data:
                buttons.data["sum"] = 0.0
                buttons.content.controls[1].value =f"${buttons.data['sum']:.2f}"        
        page.pop_dialog()
        update_total_add()

    def hide_input_view():
        input_view.visible = False
        main_view.visible = True
        page.update()


#This block will create the new text fields, dropdowns, and buttons.
    new_chore_title = ft.TextField(
        label = "New Chore Title", 
        hint_text = "What is the new chore:", 
        color=ft.Colors.ORANGE_700, 
        border_color=ft.Colors.BLACK_87, 
        border_width=2)
    
    new_chore_price = ft.TextField(
        label = "New Chore Price", 
        hint_text = "What is the price:", 
        input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",
            replacement_string=""
        ), 
        color=ft.Colors.ORANGE_700, 
        border_color=ft.Colors.BLACK_87, 
        border_width=2)
    
    submit_button = ft.ElevatedButton(
        content="SUBMIT", 
        on_click=submit,
        color=ft.Colors.ORANGE_700
    )


    exit_button = ft.ElevatedButton(
        content="Exit",
        on_click = hide_input_view
    )
    
    add_button_view = ft.ElevatedButton(
        icon=ft.Icons.ADD,
        content="Add Chore",
        on_click=show_input_view,
        color=ft.Colors.BLACK_87,
    )
                         

    main_view =ft.Column(
        controls=[
        add_button_view,
        ],
        visible = True,
    )
    
    
    input_view = ft.Column(
        controls=[
        new_chore_title,
        new_chore_price,
        ft.Row(
            controls=[
                submit_button,
                exit_button,
            ]
        )
        ],
        visible = False
    )

    #This block creates the columns.
    page.add(
        ft.Text(
            "Golly G's Chores",
            size=28,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.ORANGE_700,
        ),
        ft.Divider(height=30),   
        main_view,
        input_view,
        ft.Divider(height=30),
        chore_column,
        ft.Divider(height=30),
        ft.Column(
            controls=[
                grand_chore_total,
                ft.FloatingActionButton(
                    icon=ft.Icons.ATTACH_MONEY,
                    on_click=show_pay_chore,
                    )
            ],
        ),
    ),


#This block allows the code to be ran.
if __name__ == "__main__":
    ft.app(target=main)