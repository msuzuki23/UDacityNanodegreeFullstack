<h1>Project: Linux Server Configuration</h1>

<p>As part of the Udacity Nanodegree Full Stack Web Development, the code must be deployed/hosted on a Web Hosting Cloud.</p>
<p>This document describes the steps, set-ups and tools used for the task.</p>
<p></p>

<h2>About</h2>
<p>The chosen cloud provider is Amazon AWS.</p>
<p>A Ubuntu instance was created on the cloud host.</p>
<p>The chosen database was Postgresql.</p>
<p>An Apache Server was used as a webserver.</p>
<p>Mod_wsgi was used as a "connector" between the ItemCatalog Flask code to the Apache Server.</p>

<h2>Details</h2>
<p>Here I will describe on more details how I put all the pieces together on the cloud server.</p>

<h3>1. Create Instance on Amazon AWS Cloud</h3>
<p>First I had to go on and chose a cloud provider. I had an Amazon AWS already created on the past. Since, I already had the account, that was a simple choice to go with Amazon AWS.</p>
<p>I went on the console, and chose an EC2 Instance. Amazon will lead through the steps of creating the server.</p>
<p>I chose the Ubunut 18.04 LTS option.</p>
<p>At the end of set-up Amazon asks if you want to generate the ssh-key, I chose "yes", named the instance, and the key is downloaded into my local "Downloads" folder.</p>
<p>Then moved the ssh-key to ~/.ssh/rsa_id/</p>

<h3>2. Set-up Server</h3>
<p>Once I sshed with the ubuntu user, I followed the steps on the trainning/course.</p>
<p>First I set-up the default incoming/outgoing ports for the Firewall.</p>
<p>Then started enabling the necessary ports: SSH 2200, HTTP 80, NTP 123.</p>
<p>Also had to go into the sshd_config and change the ssh port to 2200. After I had to restart sshd (sudo service sshd restart).</p>
<p>After that I created user grader, generated the ssh_key on my local machine, set-up the permissions on the ssh_key files with chmod.</p>
<p>Then moved the ssh-key into grader's .ssh folder.</p>
<p>Tested logging-in with grader using ssh.</p>
<p>Then back to the ubuntu user, added the grader file into /etc/sudoers.d to allow user grader as sudo.</p>
<p>Logged back in as user grader, and tested the sudo.</p>

<h3>3. Installations</h3>
<p>Installed apache on server. It is important to notice the apache version, in my case 2.4, as some configurations in mod_wsgi differ from apache versions.</p>
<p>Next step I sudo installed mod_wsgi for python 3. Since my python was 3.6, I installed mod_wsgi python3. It is important to have mod_wsgi match your python version, so you won't have any errors due to python and mod_wsgi installations.</p>
<p>Next I downloaded the ItemCatalog code from my git repository. One important step is to copy your flask code under "/var/www/html/Your Dir" it seems that when apache starts the service, this is the folder apache has full access to it.</p>
<p>I also created a python virtual environment, so all the packages/libraries used for the ItemCatalog stays in the same python virtual environment. Making easier for debug when piecing together the ItemCatalog Flask code, mod_wsgi and apache together.</p>
<p>Next I set-up my mod_wsgi. Mostly I followed these instructions for installs and configuration:</p>
<p>https://www.codementor.io/abhishake/minimal-apache-configuration-for-deploying-a-flask-app-ubuntu-18-04-phu50a7ft</p>

<h3>4. Code Modifications</h3>
<p>After everything is installed, the web pages do not start/work as planned.</p>
<p>Most of errors were logged in the Apache error logs (sudo tail /var/log/apache2/error.log).</p>
<p>Sometimes missing a python library/package. This is the reason I implement python virtual environments, so I hava full control of what packages are installed and missing, making easier to debug from the Apache Error Logs.</p>
<p>Another thing I had to do is to request a new Google Oauth Authentication Token. The former Oauth Token usend of the Development code did not work, even after I changed the requesting server on the Google Oauth API Console, but it was giving me an error when the calling the login page, the error was sent on the browser console.</p>
<p>One tip is if you need to get the "print" from your Flask Code, you can use:</p>
<p>import sys</p>
<p>print("Hello World", file=sys.stderr)</p>
<p>So, your prints will go into the Apache Error Log.</p>

<h3>Conclusion</h3>
<p>From this experience of hosting the web application, I learned that no task should be downlooked. What I mean by that. Before getting into the task, I thought the hardest part, such as the coding piece had passed, and that hosting would be a "copy"paste" kind of operation.</p>
<p>I was proven completely wrong.</p>
<p>Because of that expectation, the task turned into a sometimes frustrating endeavor.</p>
<p>Now it is easier to look back with a sense of satisfaction that I was able to clear a major challenge, and that no task should be overlooked, downplayed.<p>
<p>I can attest that I learned quite a lot in this project, from setting-up the server, configuring ports and users, to glueing all pieces together with mod_wsgi.</p>