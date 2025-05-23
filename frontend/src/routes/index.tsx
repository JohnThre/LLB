import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

// Import layouts
import DashboardLayout from '../components/Dashboard/DashboardLayout';

// Import pages
import Chat from '../pages/Chat';
import Settings from '../pages/Settings';
import NotFound from '../pages/NotFound';
import Login from '../pages/Login';
import Profile from '../pages/Profile';
import ChatHistory from '../pages/Chat/ChatHistory';
import ChatSettings from '../pages/Chat/ChatSettings';
import ProfileSettings from '../pages/Profile/ProfileSettings';
import SecuritySettings from '../pages/Profile/SecuritySettings';
import GeneralSettings from '../pages/Settings/GeneralSettings';
import AppearanceSettings from '../pages/Settings/AppearanceSettings';
import NotificationSettings from '../pages/Settings/NotificationSettings';

import AnimatedPage from '../components/AnimatedPage';
import ProtectedRoute from '../components/ProtectedRoute';

const AppRoutes: React.FC = () => {
  const { t } = useTranslation();

  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      
      <Route
        path="/login"
        element={
          <AnimatedPage>
            <Login />
          </AnimatedPage>
        }
      />

      {/* Dashboard Routes */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="chat" replace />} />
        
        {/* Chat Routes */}
        <Route path="chat" element={<Chat />} />
        <Route path="chat/history" element={<ChatHistory />} />
        <Route path="chat/settings" element={<ChatSettings />} />

        {/* Profile Routes */}
        <Route path="profile" element={<Profile />} />
        <Route path="profile/settings" element={<ProfileSettings />} />
        <Route path="profile/security" element={<SecuritySettings />} />

        {/* Settings Routes */}
        <Route path="settings" element={<Settings />}>
          <Route index element={<GeneralSettings />} />
          <Route path="appearance" element={<AppearanceSettings />} />
          <Route path="notifications" element={<NotificationSettings />} />
        </Route>
      </Route>

      {/* 404 Route */}
      <Route
        path="*"
        element={
          <AnimatedPage>
            <NotFound />
          </AnimatedPage>
        }
      />
    </Routes>
  );
};

export default AppRoutes; 