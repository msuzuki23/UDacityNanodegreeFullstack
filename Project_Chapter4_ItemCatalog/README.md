<h1>Item Catalog Project</h1>
  <p>This git holds all the modules and code related to Item Catalog project for Udacity Nanodegree Full Stack Developer.</p>

<h2>About</h2>
  <p>The application provides a list of items, in this case companies where user can interact with the cars made by the related companies.</p>
  <p>User must be authenticated and logged-in in order to perform add/edit/delete of cars.</p>
  <p>Authentication users Google and Facebook oauth authorization.</p>

<h2>Features</h2>
  <ul>
    <li>Authentication using oauth api, Google and Facebook</li>
    <li>CRUD Operations using Flask and SQLAlchemy</li>
    <li>Rest API with JSON endpoints</li>
  </ul>

<h2>Project set-up</h2>
  <p>The OS that was used for this project is Ubuntu 18.04LTS. Some minor adjustment maybe needed in case you are running a Windows machine, such as directory paths.</p>
  <p>The database used for this project is postgresql.</p>
  <p>The python version used for this project is 3.6.8.</p>
    <ul>
        <ol>To create and grant access to the tables the SQL Commands are located in file Postgres_Database.</ol>
        <ol>After the tables and permissions are set in the DB. Run python script "seed.py" to iniatilly seed the tables in the database.</ol>
        <ol>The entry script/code to the application is app.py. app.py provides all the "links" to the application Blueprints.</ol>
    </ul>
    <p>Flask Blueprints were used for this project to keep the code better organized and compartimentalized according to the functionality.</p>
