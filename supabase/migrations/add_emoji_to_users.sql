-- Migration: Add emoji column to users table
-- Run this in Supabase SQL Editor or via CLI

ALTER TABLE public.users ADD COLUMN emoji TEXT;