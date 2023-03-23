import geni.portal as portal
import geni.rspec.pg as rspec

# Create a Request object to start building the RSpec.
request = portal.context.makeRequestRSpec()
# Create a XenVM
node = request.XenVM("node")
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU20-64-STD"
node.routable_control_ip = "true"

node.addService(rspec.Execute(shell="/bin/sh", command="sudo apt update"))
#node.addService(rspec.Execute(shell="/bin/sh", command="sudo apt install -y nginx"))
node.addService(rspec.Execute(shell="/bin/sh", command="sudo apt install -y apache2"))
node.addService(rspec.Execute(shell="/bin/sh", command='sudo systemctl status apache2'))
node.addService(rspec.Execute(shell="/bin/sh", command='sudo ufw allow "Apache Full"'))
node.addService(rspec.Execute(shell="/bin/sh", command='a2enmod ssl'))
node.addService(rspec.Execute(shell="/bin/sh", command='systemctl restart apache2'))
node.addService(rspec.Execute(shell="/bin/sh", command='sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt'))
node.addService(rspec.Execute(shell="/bin/sh", command='sudo nano /etc/apache2/sites-available/pcvm605-4.emulab.net.config'))

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()
