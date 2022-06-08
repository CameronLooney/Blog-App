from app import app

# in terminal to run
# export FLASK_APP=blog.py
# export FLASK_ENV=development
#  flask run
# flask db init
# flask db migrate -m "Database table name"

'''
HTML COMMENTS
Login.html 
 <!-- <form> element is used as a container for the web form.-->

<!--     action attribute of the form is used to tell the browser-->
<!--     the URL that should be used when submitting the information the user entered in the form.-->

<!--     When the action is set to an empty string the form is submitted to the URL that is currently in the address bar-->

<!--     The method attribute specifies the HTTP request method that should be used when submitting the form to the server.-->

<!--     The novalidate attribute is used to tell the web browser to not apply validation to the fields in this form (for testing)-->

<!--      form.hidden_tag() used to protect the form against CSRF attacks.-->

<!--      {{ form.<field_name>.label }} where I wanted the field label, and {{ form.<field_name>() }} where I wanted the field.-->
'''