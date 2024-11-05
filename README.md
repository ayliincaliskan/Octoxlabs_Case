# Octoxlabs Case

## Local development
1. Install Docker.
2. From the repo's root run: `source tools/docker-development.sh`.
3. Run initial migrations: `python manage.py migrate`.

## Running tests on local
To run all tests:
1. `source unittest.sh`

## Technologies Used
1. Django
2. Docker
3. Redis
4. SQlite
5. Elasticsearch

## Project Content
- API was developed to create users and jwt was used here.
- Redis was used as the queue, and the actions taken were written to - redis.
- worker service was added, this service took actions from redist and wrote them to elasticsearch.
- A Post model and Tag model were created. create, update, delete and list functions were written for these models.
- Unit tests were written for functions

## API Endpoints
### Create Account
- URL: /api/account/user-create/
- METHOD: POST
#### Request Body
```bash
{
    "username": "exampleuser",
    "password": "your-password-here"
    "email": "user@example.com"
}
```
#### Response
```bash
{
    "access_token": "your-access-token-here",
    "refresh_token": "your-refresh-token-here"
}
```
### Login
- URL: 
- METHOD: POST
#### Request Body
```bash
{
    "username": "exampleuser",
    "password": "your-password-here"
}
```
#### Response
```bash
{
    "access_token": "your-access-token-here",
    "refresh_token": "your-refresh-token-here"
}
```
### User List
- URL: /api/account/user-list/
- METHOD: GET
#### Request Auth
```bash
{
    authorization: "Bearer your-access-token-here",
}
```
#### Response
```bash
[
	{
		"id": 1,
		"username": "exampleuser",
		"email": "user@example.com"
	}
]
```
### User Get
- URL: /api/account/users/1
- METHOD: GET
#### Request Auth
```bash
{
    authorization: "Bearer your-access-token-here",
}
```
#### Response
```bash
{
	"id": 1,
	"username": "exampleuser",
	"email": "user@example.com"
}
```
#### User Delete
- URL: /api/account/users/1/
- METHOD: DELETE
#### Request Auth
```bash
{
    authorization: "Bearer your-access-token-here",
}
```
#### Response
```bash
{
    status_code: 204
}
```
#### Create Post
- URL: /api/blog/post-create/
- METHOD: POST
#### Request Body
```bash
{
	"title": "Post_1", 
	"content": "Bu postun içeriği."
}
```
#### Request Auth
```bash
{
    authorization: "Bearer your-access-token-here",
}
```
#### Response
```bash
{
	"id": 1,
	"title": "Post_1",
	"content": "Bu postun içeriği.",
	"tags": [],
	"created_at": "2024-11-04T02:06:59.514896Z",
	"updated_at": "2024-11-04T02:06:59.514912Z"
}
```
#### Get Post
- URL: /api/blog/posts/1
- METHOD: GET
#### Request Auth
```bash
{
    authorization: "Bearer your-access-token-here",
}
```
#### Response
```bash
{
	"id": 1,
	"title": "Post_1",
	"content": "Bu postun içeriği.",
	"tags": [],
	"created_at": "2024-11-04T02:06:59.514896Z",
	"updated_at": "2024-11-04T02:06:59.514912Z"
}
```
### Post List
- URL: /api/blog/post-list/
- METHOD: GET
#### Request Auth
```bash
{
    authorization: "Bearer your-access-token-here",
}
```
#### Response
```bash
[
	{
		"id": 1,
		"title": "Post_1",
		"content": "Bu postun içeriği.",
		"tags": [],
		"created_at": "2024-11-04T01:58:57.600825Z",
		"updated_at": "2024-11-04T01:58:57.600851Z"
	}
]
```
#### Post Delete
- URL: /api/blog/posts/1/
- METHOD: DELETE
#### Request Auth
```bash
{
    authorization: "Bearer your-access-token-here",
}
```
#### Response
```bash
{
    status_code: 204
}
```
### Post Update
- URL: /api/blog/posts/1/
- METHOD: PUT
#### Request Body
```bash
{
	"id": 1,
	"title": "Post_22",
	"content": "Bu postun içeriği.",
	"tags": [
        {
            "name" : "Python"
            }
        ],
	"created_at": "2024-11-03T00:27:43.339197Z",
	"updated_at": "2024-11-03T00:27:43.339240Z"
}
```
#### Request Auth
```bash
{
    authorization: "Bearer your-access-token-here",
}
```
#### Response
```bash
{
	"id": 1,
	"title": "Post_22",
	"content": "Bu postun içeriği.",
	"tags": [
		{
			"id": 1,
			"name": "Python",
			"created_at": "2024-11-05T10:08:11.829444Z",
			"updated_at": "2024-11-05T10:08:11.829462Z"
		}
	],
	"created_at": "2024-11-04T02:05:37.773363Z",
	"updated_at": "2024-11-05T10:08:42.588642Z"
}
```



#### Create Tag
- URL: /api/blog/tag-create/
- METHOD: POST
#### Request Body
```bash
{
  "name": "Django"
}
```
#### Request Auth
```bash
{
    authorization: "Bearer your-access-token-here",
}
```
#### Response
```bash
{
	"id": 1,
	"name": "Django",
	"created_at": "2024-11-04T01:59:31.221460Z",
	"updated_at": "2024-11-04T01:59:31.221489Z"
}
```
#### Get Tag
- URL: /api/blog/tags/1
- METHOD: GET
#### Request Auth
```bash
{
    authorization: "Bearer your-access-token-here",
}
```
#### Response
```bash
[
	{
		"id": 1,
		"name": "Django",
		"created_at": "2024-11-04T01:59:31.221460Z",
		"updated_at": "2024-11-04T01:59:31.221489Z"
	}
]
```
### Tag List
- URL: /api/blog/tag-list/
- METHOD: GET
#### Request Auth
```bash
{
    authorization: "Bearer your-access-token-here",
}
```
#### Response
```bash
[
	{
		"id": 1,
		"name": "Django",
		"created_at": "2024-11-04T01:01:42.400526Z",
		"updated_at": "2024-11-04T01:06:34.603661Z"
	},
	{
		"id": 2,
		"name": "Python",
		"created_at": "2024-11-04T01:04:25.926986Z",
		"updated_at": "2024-11-04T01:04:25.927020Z"
	}
]
```
#### Tag Delete
- URL: /api/blog/tags/1
- METHOD: DELETE
#### Request Auth
```bash
{
    authorization: "Bearer your-access-token-here",
}
```
#### Response
```bash
{
    status_code: 204
}
```
### Tag Update
- URL: /api/blog/tags/1/
- METHOD: PUT
#### Request Body
```bash
{
		"name": "Redis"
}
```
#### Request Auth
```bash
{
    authorization: "Bearer your-access-token-here",
}
```
#### Response
```bash
{
	"id": 1,
	"name": "Redis",
	"created_at": "2024-11-05T10:08:11.829444Z",
	"updated_at": "2024-11-05T10:15:09.269856Z"
}
```
### Source List
- URL: /api/search/
- METHOD: GET
#### Request Auth
```bash
{
    authorization: "Bearer your-access-token-here",
}
```
#### Response
```bash
[
	{
		"action": "User created successfully.",
		"user": "exampleuser"
	},
	{
		"action": "Post created successfully.",
		"user": "exampleuser"
	}
]
```