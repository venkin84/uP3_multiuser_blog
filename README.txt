Project: Multi User Blog
Date: 23-Jun-16
Ver: 1.0.0.0

This is a multiuser blog application done as a part of training course @Udacity.

The expectation was that a multiuser blog application be developed for the provided
specification and demonstrates the skills learned during the course...

This web application is fully responsive and uses bootstrap framework...

The Features in this application include
-> Authenticating an user
   - Signing up a user
   - Signing in a user
   - Keeping a user signed in for a long period even if the session is closed
   - Ensuring only the authenticated user is able to use any feature of this blog
-> Blogging
   - Creating a blog
   - Viewing a blog
   - Editing a blog by its author only
   - Deleting a blog by its author only
-> Commenting
   - To comment a blog
   - To view others comments on a blog
   - To edit one's own comment on a blog
   - To delete one's own comment on a blog
   - To view overall number of comments on a blog
-> Like a blog
   - To like other's blog
   - To view overall number of likes for a blog

To run this application Google App Engine and an account in the Google Cloud Platform
is needed... Follow the steps below to run this application...
   1- Create a project in the Google Cloud Platform [GCP]
   2- Edit the app.yaml file with the project name provided in the GCP
   3- Load the project to the Google App Engine [GAE]
   4- Deploy it to the GCP
   5- Access the application url to verify successful deployment
