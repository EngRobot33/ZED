
# ZED API

This is a reference to ZED API v1





## User

### User authentication

```http
  POST /api/v1/token
```
Pass parameters as `JSON` in body
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. Username  |
| `password` | `string` | **Required**. Password  |

#### Response

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `access` | `string` |  access token to authenticate user |
| `refresh` | `string` | refresh token to refresh access token  |

```http
  POST /api/v1/refresh
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `refresh` | `string` | **Required**. refresh token to get new access token  |


#### Response

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `access` | `string` |  access token to authenticate user |

### User Profile

#### Retrieve User Profile
- **URL:** `/api/v1/user/profile`
- **Method:** `GET`
- **Description:** Retrieves authenticated user profile
- **Authentication:** Required
- **Response:**
   Returns user profile.
  

Example using curl:
```bash
curl -X GET \
  -H "Authorization: Bearer <access_token>" \
  http://example.com/api/v1/user/profile
```

### User Posts

#### Retrieve User Posts
- **URL:** `/api/v1/user/posts`
- **Method:** `GET`
- **Description:** Retrieves authenticated user posts
- **Authentication:** Required
- **Response:**
   Returns user posts in pagination.
  

Example using curl:
```bash
curl -X GET \
  -H "Authorization: Bearer <access_token>" \
  http://example.com/api/v1/user/posts
```

 ### User Follower list

#### Retrieve User follower list
- **URL:** `/api/v1/user/followerlist`
- **Method:** `GET`
- **Description:** Retrieves authenticated user follower list
- **Authentication:** Required
- **Response:**
   Returns user follower list.
  

Example using curl:
```bash
curl -X GET \
  -H "Authorization: Bearer <access_token>" \
  http://example.com/api/v1/user/followerlist
```

 ### User Following list

#### Retrieve User following list
- **URL:** `/api/v1/user/followinglist`
- **Method:** `GET`
- **Description:** Retrieves authenticated user following list
- **Authentication:** Required
- **Response:**
   Returns user following list
  

Example using curl:
```bash
curl -X GET \
  -H "Authorization: Bearer <access_token>" \
  http://example.com/api/v1/user/followinglist
```
 ### User suggestions

#### Retrieve User Topic and who to follow data
- **URL:** `/api/v1/user/suggestions`
- **Method:** `GET`
- **Description:** Retrieves authenticated user suggestions
- **Authentication:** Required
- **Response:**
   Returns user suggestions

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `follow_suggests` | `array of user` | List of users suggested to follow |
| `topics_suggest` | `array of topics` | List of topics suggested |


  

Example using curl:
```bash
curl -X GET \
  -H "Authorization: Bearer <access_token>" \
  http://example.com/api/v1/user/suggestions
```