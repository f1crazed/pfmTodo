
#!/bin/bash

#start mondodb
service mongodb start &
#start the flask app
flask run --host 0.0.0.0