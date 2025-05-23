import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
  useTheme,
  useMediaQuery,
  Breadcrumbs,
  Link,
} from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import ChatIcon from '@mui/icons-material/Chat';
import SettingsIcon from '@mui/icons-material/Settings';
import MenuIcon from '@mui/icons-material/Menu';
import { useAuth } from '../contexts/AuthContext';

interface HeaderProps {
  onMenuClick?: () => void;
}

const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useTranslation();
  const { logout } = useAuth();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const navItems = [
    { path: '/dashboard/chat', label: t('nav.chat'), icon: <ChatIcon /> },
    { path: '/dashboard/settings', label: t('nav.settings'), icon: <SettingsIcon /> },
  ];

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const generateBreadcrumbs = () => {
    const paths = location.pathname.split('/').filter(Boolean);
    const breadcrumbs = paths.map((path, index) => {
      const url = `/${paths.slice(0, index + 1).join('/')}`;
      const label = t(`nav.${path}`, { defaultValue: path });
      return { label, url };
    });

    return breadcrumbs;
  };

  return (
    <AppBar 
      position="static" 
      color="primary" 
      elevation={0}
      sx={{
        borderBottom: 1,
        borderColor: 'divider',
      }}
    >
      <Toolbar>
        {isMobile && (
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={onMenuClick}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
        )}

        <Typography
          variant="h6"
          component="div"
          sx={{ 
            flexGrow: 1, 
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: 2,
          }}
          onClick={() => navigate('/dashboard')}
        >
          LLB
          {!isMobile && (
            <Breadcrumbs 
              aria-label="breadcrumb"
              sx={{ 
                color: 'inherit',
                '& .MuiBreadcrumbs-separator': {
                  color: 'inherit',
                },
              }}
            >
              {generateBreadcrumbs().map((crumb, index) => (
                <Link
                  key={crumb.url}
                  color="inherit"
                  underline="hover"
                  onClick={(e) => {
                    e.stopPropagation();
                    navigate(crumb.url);
                  }}
                  sx={{ 
                    cursor: 'pointer',
                    opacity: 0.8,
                    '&:hover': {
                      opacity: 1,
                    },
                  }}
                >
                  {crumb.label}
                </Link>
              ))}
            </Breadcrumbs>
          )}
        </Typography>

        {!isMobile && (
          <Box sx={{ display: 'flex', gap: 2 }}>
            {navItems.map((item) => (
              <Button
                key={item.path}
                color="inherit"
                startIcon={item.icon}
                onClick={() => navigate(item.path)}
                sx={{
                  backgroundColor: location.pathname === item.path 
                    ? 'rgba(255, 255, 255, 0.1)' 
                    : 'transparent',
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.2)',
                  },
                }}
              >
                {item.label}
              </Button>
            ))}
          </Box>
        )}

        <Button
          color="inherit"
          onClick={handleLogout}
          sx={{ 
            ml: 2,
            '&:hover': {
              backgroundColor: 'rgba(255, 255, 255, 0.1)',
            },
          }}
        >
          {t('auth.logout')}
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default Header; 