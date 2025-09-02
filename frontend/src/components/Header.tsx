import React from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
  useTheme,
  useMediaQuery,
} from "@mui/material";
import { useNavigate, useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";
import ChatIcon from "@mui/icons-material/Chat";
import SettingsIcon from "@mui/icons-material/Settings";
import MenuIcon from "@mui/icons-material/Menu";
import { useAuth } from "../contexts/AuthContext";
import { bauhausColors } from "../theme";

interface HeaderProps {
  onMenuClick?: () => void;
}

const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useTranslation();
  const { logout } = useAuth();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));

  const navItems = [
    { path: "/dashboard/chat", label: t("nav.chat"), icon: <ChatIcon /> },
    {
      path: "/dashboard/settings",
      label: t("nav.settings"),
      icon: <SettingsIcon />,
    },
  ];

  const handleLogout = async () => {
    try {
      await logout();
      navigate("/login");
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <AppBar
      position="static"
      elevation={0}
      sx={{
        backgroundColor: bauhausColors.white,
        color: bauhausColors.black,
        borderBottom: `4px solid ${bauhausColors.blue}`,
      }}
    >
      <Toolbar sx={{ minHeight: "80px !important", px: 3 }}>
        {isMobile && (
          <IconButton
            aria-label="open drawer"
            edge="start"
            onClick={onMenuClick}
            sx={{ 
              mr: 2,
              color: bauhausColors.black,
              border: `2px solid ${bauhausColors.black}`,
              borderRadius: 0,
              "&:hover": {
                backgroundColor: bauhausColors.yellow,
              },
            }}
          >
            <MenuIcon />
          </IconButton>
        )}

        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            cursor: "pointer",
            "&:hover": {
              "& .logo-text": {
                color: bauhausColors.red,
              },
            },
          }}
          onClick={() => navigate("/dashboard")}
        >
          <Box
            sx={{
              width: 40,
              height: 40,
              backgroundColor: bauhausColors.red,
              mr: 2,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              border: `2px solid ${bauhausColors.black}`,
            }}
          >
            <Typography
              variant="h6"
              sx={{
                color: bauhausColors.white,
                fontWeight: 700,
                fontSize: "1.2rem",
              }}
            >
              L
            </Typography>
          </Box>
          <Typography
            variant="h4"
            component="div"
            className="logo-text"
            sx={{
              fontWeight: 700,
              letterSpacing: "0.1em",
              color: bauhausColors.black,
              transition: "color 0.15s ease",
            }}
          >
            LLB
          </Typography>
        </Box>

        <Box sx={{ flexGrow: 1 }} />

        {!isMobile && (
          <Box sx={{ display: "flex", gap: 0 }}>
            {navItems.map((item, index) => (
              <Button
                key={item.path}
                startIcon={item.icon}
                onClick={() => navigate(item.path)}
                sx={{
                  backgroundColor:
                    location.pathname === item.path
                      ? bauhausColors.yellow
                      : "transparent",
                  color: bauhausColors.black,
                  border: `2px solid ${bauhausColors.black}`,
                  borderRadius: 0,
                  borderLeft: index > 0 ? "none" : `2px solid ${bauhausColors.black}`,
                  "&:hover": {
                    backgroundColor: bauhausColors.yellow,
                  },
                }}
              >
                {item.label}
              </Button>
            ))}
          </Box>
        )}

        <Button
          onClick={handleLogout}
          sx={{
            ml: 2,
            backgroundColor: bauhausColors.red,
            color: bauhausColors.white,
            border: `2px solid ${bauhausColors.black}`,
            borderRadius: 0,
            "&:hover": {
              backgroundColor: bauhausColors.black,
              color: bauhausColors.white,
            },
          }}
        >
          {t("auth.logout")}
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default Header;