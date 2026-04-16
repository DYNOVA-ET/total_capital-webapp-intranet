# Row Level Security (RLS) Documentation

## Overview
This document outlines the Row Level Security policies implemented in the Total Capital Intranet Supabase database.

## Tables with RLS Enabled

### 1. `audit_logs`
- **RLS Enabled**: Yes
- **Policies**:
  - Users can view their own audit logs
  - Admins can view all audit logs
- **Purpose**: Track user actions for compliance and debugging

### 2. `users`
- **RLS Enabled**: Yes (assumed)
- **Policies**: 
  - Users can read/update their own profile
  - Admins can read/update all users
- **Purpose**: User management

### 3. `user_departments`
- **RLS Enabled**: Yes (assumed)
- **Policies**:
  - Users can view their department assignments
  - Admins can manage all assignments
- **Purpose**: Department-based access control

### 4. `departments`
- **RLS Enabled**: Yes (assumed)
- **Policies**:
  - All authenticated users can read departments
  - Admins can manage departments
- **Purpose**: Department metadata

### 5. `roles`
- **RLS Enabled**: Yes (assumed)
- **Policies**:
  - All authenticated users can read roles
  - Admins can manage roles
- **Purpose**: Role definitions

## Testing RLS Policies

Run these SQL queries in Supabase SQL Editor to verify RLS is working:

```sql
-- Test 1: Non-admin user cannot see other users' audit logs
-- (Run as regular user)
SELECT * FROM audit_logs WHERE user_id != auth.uid();

-- Should return 0 rows

-- Test 2: Admin can see all audit logs
-- (Run as admin user)
SELECT COUNT(*) FROM audit_logs;

-- Should return actual count

-- Test 3: User can only see their own profile
-- (Run as regular user)
SELECT * FROM users WHERE id != auth.uid();

-- Should return 0 rows
```

## Maintenance
- Review policies annually
- Update policies when adding new tables
- Test policies after schema changes