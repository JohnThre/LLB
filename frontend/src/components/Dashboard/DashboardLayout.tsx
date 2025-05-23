import React from 'react';
import {
  Box,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Divider,
  Typography,
  Collapse,
} from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import DashboardIcon from '@mui/icons-material/Dashboard';
import PersonIcon from '@mui/icons-material/Person';
import SecurityIcon from '@mui/icons-material/Security';
import ChatIcon from '@mui/icons-material/Chat';
import HistoryIcon from '@mui/icons-material/History';
import SettingsIcon from '@mui/icons-material/Settings';
import PaletteIcon from '@mui/icons-material/Palette';
import NotificationsIcon from '@mui/icons-material/Notifications';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import Layout from '../Layout';

interface MenuItem {
  title: string;
  path: string;
  icon: React.ReactNode;
  subItems?: MenuItem[];
}

interface DividerItem {
  type: 'divider';
}

type MenuItemType = MenuItem | DividerItem;

const isMenuItem = (item: MenuItemType): item is MenuItem => {
  return 'path' in item;
}

const DashboardLayout: React.FC<{ children: React.ReactNode }> = ({ 
  children 
}) => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();
  const [openSections, setOpenSections] = React.useState<{
    [key: string]: boolean;
  }>({
    chat: true,
    profile: true,
    settings: true,
  });

  const menuItems: MenuItemType[] = [
    {
      title: t('nav.chat'),
      path: '/dashboard/chat',
      icon: <ChatIcon />,
      subItems: [
        {
          title: t('nav.chatHistory'),
          path: '/dashboard/chat/history',
          icon: <HistoryIcon />,
        },
        {
          title: t('nav.chatSettings'),
          path: '/dashboard/chat/settings',
          icon: <SettingsIcon />,
        },
      ],
    },
    { type: 'divider' },
    {
      title: t('nav.profile'),
      path: '/dashboard/profile',
      icon: <PersonIcon />,
      subItems: [
        {
          title: t('nav.profileSettings'),
          path: '/dashboard/profile/settings',
          icon: <SettingsIcon />,
        },
        {
          title: t('nav.security'),
          path: '/dashboard/profile/security',
          icon: <SecurityIcon />,
        },
      ],
    },
    { type: 'divider' },
    {
      title: t('nav.generalSettings'),
      path: '/dashboard/settings',
      icon: <SettingsIcon />,
      subItems: [
        {
          title: t('nav.appearance'),
          path: '/dashboard/settings/appearance',
          icon: <PaletteIcon />,
        },
        {
          title: t('nav.notifications'),
          path: '/dashboard/settings/notifications',
          icon: <NotificationsIcon />,
        },
      ],
    },
  ];

  const handleSectionClick = (section: string) => {
    setOpenSections(prev => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  const renderMenuItem = (item: MenuItem, level: number = 0) => {
    const isActive = location.pathname === item.path;
    const hasSubItems = item.subItems && item.subItems.length > 0;
    const section = item.path.split('/')[2];

    return (
      <React.Fragment key={item.path}>
        <ListItem disablePadding>
          <ListItemButton
            selected={isActive}
            onClick={() => {
              if (hasSubItems) {
                handleSectionClick(section);
              } else {
                navigate(item.path);
              }
            }}
            sx={{
              pl: level * 2 + 2,
              '&.Mui-selected': {
                backgroundColor: 'action.selected',
                '&:hover': {
                  backgroundColor: 'action.selected',
                },
              },
            }}
          >
            <ListItemIcon sx={{ minWidth: 40 }}>{item.icon}</ListItemIcon>
            <ListItemText 
              primary={
                <Typography variant="body2" sx={{ fontWeight: isActive ? 600 : 400 }}>
                  {item.title}
                </Typography>
              } 
            />
            {hasSubItems && (
              openSections[section] ? <ExpandLess /> : <ExpandMore />
            )}
          </ListItemButton>
        </ListItem>
        {hasSubItems && (
          <Collapse in={openSections[section]} timeout="auto" unmountOnExit>
            <List component="div" disablePadding>
              {item.subItems?.map(subItem => renderMenuItem(subItem, level + 1))}
            </List>
          </Collapse>
        )}
      </React.Fragment>
    );
  };

  const drawer = (
    <Box sx={{ overflow: 'auto' }}>
      <List>
        {menuItems.map((item, index) => {
          if (!isMenuItem(item)) {
            return <Divider key={index} />;
          }
          return renderMenuItem(item);
        })}
      </List>
    </Box>
  );

  return (
    <Layout showDrawer drawerContent={drawer}>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.3 }}
      >
        <Paper
          elevation={0}
          sx={{
            p: 3,
            borderRadius: 2,
            backgroundColor: 'background.paper',
            minHeight: 'calc(100vh - 64px)',
          }}
        >
          {children}
        </Paper>
      </motion.div>
    </Layout>
  );
};

export default DashboardLayout; 