# Mentor App Backend

## How to Setup

## Test
1. Run all tests.
```
coverage run manage.py test
```

2. Run a specefic Tests File.
```
python manage.py test myapp.tests.test_views
```

3. Run a Specific Tests class
```
python manage.py test path.to.your.test_module.TestClassName
```

For example, if you want to run a specific test class named MyViewTest in myapp/tests/test_views.py, you can run:
```
python manage.py test myapp.tests.test_views.MyViewTest
```

4. Get the Tests coverage Report.
```
coverage report
```

5. Get the TestS Coverage in HTML
```
coverage html
```

## API Documentation

| App           | Description      | Endpoint               | Method     | Payload/ Params                             |
|---------------|------------------|------------------------|------------|---------------------------------------------|
| Profile       |create profile    | user/create_profile/   | POST       | `{"birth_day": "1993-04-23","gender": "male","country": "Sri Lanka","educational_level": "school","tags": [1],"subjects": [],"topics": [1]}`|
|               | get profile      | user/profile_detail/   | GET        |                                             |
|               | Update Profile   | user/profile_detail/   | PUT/PATCH  | `{"birth_day": "1993-04-23","gender": "male","country": "Sri Lanka","educational_level": "school","tags": [1],"subjects": [],"topics": [1]}`|
| Subject       | get subjects     | user/get_subjects/     | GET        | `title=something`                           |
|               | create subject   | user/create_subject/   | POST       | `{"title":"Test"}`                          |
| Tag           | create tag       | user/create_tag/       | POST       | `{"title": "title"}`                        |