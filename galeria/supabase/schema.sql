-- CB Grup Barna Galeria - Database Schema
-- Run this in your Supabase SQL editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Profiles (extends auth.users)
CREATE TABLE public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name TEXT,
  role TEXT DEFAULT 'viewer' CHECK (role IN ('viewer', 'contributor', 'editor', 'admin')),
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Seasons
CREATE TABLE public.seasons (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE, -- e.g. "2024-2025"
  is_active BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Events
CREATE TABLE public.events (
  id SERIAL PRIMARY KEY,
  season_id INTEGER REFERENCES public.seasons(id) ON DELETE SET NULL,
  title TEXT NOT NULL,
  description TEXT,
  event_date DATE,
  location TEXT,
  cover_photo_id INTEGER,
  allow_downloads BOOLEAN DEFAULT TRUE,
  allow_member_uploads BOOLEAN DEFAULT TRUE,
  is_published BOOLEAN DEFAULT TRUE,
  created_by UUID REFERENCES public.profiles(id),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Photos
CREATE TABLE public.photos (
  id SERIAL PRIMARY KEY,
  event_id INTEGER REFERENCES public.events(id) ON DELETE CASCADE,
  storage_path TEXT NOT NULL,
  thumbnail_path TEXT,
  original_name TEXT,
  caption TEXT,
  width INTEGER,
  height INTEGER,
  file_size INTEGER,
  uploaded_by UUID REFERENCES public.profiles(id),
  uploaded_at TIMESTAMPTZ DEFAULT NOW(),
  likes_count INTEGER DEFAULT 0,
  is_approved BOOLEAN DEFAULT TRUE
);

-- Add foreign key for cover photo after photos table exists
ALTER TABLE public.events
  ADD CONSTRAINT events_cover_photo_fk
  FOREIGN KEY (cover_photo_id) REFERENCES public.photos(id) ON DELETE SET NULL;

-- Photo likes
CREATE TABLE public.photo_likes (
  photo_id INTEGER REFERENCES public.photos(id) ON DELETE CASCADE,
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (photo_id, user_id)
);

-- Comments
CREATE TABLE public.comments (
  id SERIAL PRIMARY KEY,
  photo_id INTEGER REFERENCES public.photos(id) ON DELETE CASCADE,
  user_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_photos_event_id ON public.photos(event_id);
CREATE INDEX idx_events_season_id ON public.events(season_id);
CREATE INDEX idx_comments_photo_id ON public.comments(photo_id);

-- Row Level Security
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.seasons ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.photos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.photo_likes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.comments ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Profiles are viewable by authenticated users"
  ON public.profiles FOR SELECT TO authenticated USING (true);
CREATE POLICY "Users can update own profile"
  ON public.profiles FOR UPDATE TO authenticated USING (auth.uid() = id);
CREATE POLICY "Users can insert own profile"
  ON public.profiles FOR INSERT TO authenticated WITH CHECK (auth.uid() = id);

-- Seasons policies (public read, admin write)
CREATE POLICY "Seasons are publicly viewable"
  ON public.seasons FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Admins can manage seasons"
  ON public.seasons FOR ALL TO authenticated
  USING (EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role = 'admin'));

-- Events policies (published events are public)
CREATE POLICY "Published events are publicly viewable"
  ON public.events FOR SELECT TO anon, authenticated USING (is_published = true);
CREATE POLICY "Editors and admins can manage events"
  ON public.events FOR ALL TO authenticated
  USING (EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('editor', 'admin')));

-- Photos policies
CREATE POLICY "Approved photos are publicly viewable"
  ON public.photos FOR SELECT TO anon, authenticated USING (is_approved = true);
CREATE POLICY "Contributors can upload photos"
  ON public.photos FOR INSERT TO authenticated
  WITH CHECK (
    uploaded_by = auth.uid() AND
    EXISTS (
      SELECT 1 FROM public.profiles p
      JOIN public.events e ON e.id = event_id
      WHERE p.id = auth.uid()
      AND (p.role IN ('contributor', 'editor', 'admin') OR e.allow_member_uploads = true)
    )
  );
CREATE POLICY "Users can delete own photos, editors+ can delete any"
  ON public.photos FOR DELETE TO authenticated
  USING (
    uploaded_by = auth.uid() OR
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('editor', 'admin'))
  );

-- Photo likes policies
CREATE POLICY "Likes are viewable by all"
  ON public.photo_likes FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Authenticated users can like"
  ON public.photo_likes FOR INSERT TO authenticated WITH CHECK (user_id = auth.uid());
CREATE POLICY "Users can unlike own likes"
  ON public.photo_likes FOR DELETE TO authenticated USING (user_id = auth.uid());

-- Comments policies
CREATE POLICY "Comments are publicly viewable"
  ON public.comments FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Authenticated users can comment"
  ON public.comments FOR INSERT TO authenticated WITH CHECK (user_id = auth.uid());
CREATE POLICY "Users can delete own comments, admins can delete any"
  ON public.comments FOR DELETE TO authenticated
  USING (
    user_id = auth.uid() OR
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role = 'admin')
  );

-- Function: auto-create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, full_name, role)
  VALUES (NEW.id, NEW.raw_user_meta_data->>'full_name', 'viewer');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Function: update likes_count on photo
CREATE OR REPLACE FUNCTION public.update_photo_likes_count()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    UPDATE public.photos SET likes_count = likes_count + 1 WHERE id = NEW.photo_id;
  ELSIF TG_OP = 'DELETE' THEN
    UPDATE public.photos SET likes_count = likes_count - 1 WHERE id = OLD.photo_id;
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_photo_like_change
  AFTER INSERT OR DELETE ON public.photo_likes
  FOR EACH ROW EXECUTE FUNCTION public.update_photo_likes_count();

-- Storage bucket (run after creating the bucket in Supabase dashboard)
-- INSERT INTO storage.buckets (id, name, public) VALUES ('photos', 'photos', true);
