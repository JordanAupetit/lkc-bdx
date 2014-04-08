
# Tool for compiling a Linux kernel #

## Application ##

You can launch the application (GTK) via the main.py file 
in the "application" folder.

==> python2 application/main.py

or 

==> python2 application/main.py ~/home/user/linux-3.13 x86 x86_64 ~/home/user/.config

## Unit tests ##

You can run our test script to verify the performance of our functions.
This script is in the folder application/core.

==> python2 application/core/unit_tests.py ~/path/to/your/linux/kernel


## Documentation ##

You can find documentation on the two main classes in the doc folder. 
You will also find our report latex.


## Website ##

You can find scripts of the site in the website folder to change its hosting. 
In the folder "website/sql" there is the script to create the MySQL database. 
Finally, the file "website/views/connectBD.php" to edit is finally connect 
with the right database.











