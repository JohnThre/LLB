import React, { useState } from "react";
import {
  Box,
  Container,
  Typography,
  Drawer,
  useTheme,
  useMediaQuery,
} from "@mui/material";
import { useTranslation } from "react-i18next";
import { useLocation } from "react-router-dom";
import { AnimatePresence } from "framer-motion";
import Header from "../Header";

const DRAWER_WIDTH = 240;

interface LayoutProps {
  children: React.ReactNode;
  showDrawer?: boolean;
  drawerContent?: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({
  children,
  showDrawer = false,
  drawerContent,
}) => {
  const { t } = useTranslation();
  const location = useLocation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  return (
    <Box sx={{ display: "flex", minHeight: "100vh" }}>
      {showDrawer && (
        <Box
          component="nav"
          sx={{ width: { sm: DRAWER_WIDTH }, flexShrink: { sm: 0 } }}
        >
          <Drawer
            variant={isMobile ? "temporary" : "permanent"}
            open={isMobile ? mobileOpen : true}
            onClose={handleDrawerToggle}
            ModalProps={{
              keepMounted: true, // Better open performance on mobile
            }}
            sx={{
              "& .MuiDrawer-paper": {
                boxSizing: "border-box",
                width: DRAWER_WIDTH,
              },
            }}
          >
            {drawerContent}
          </Drawer>
        </Box>
      )}
      <Box sx={{ display: "flex", flexDirection: "column", flexGrow: 1 }}>
        <Header onMenuClick={handleDrawerToggle} />
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 3,
            width: showDrawer
              ? { sm: `calc(100% - ${DRAWER_WIDTH}px)` }
              : "100%",
          }}
        >
          <AnimatePresence mode="wait">{children}</AnimatePresence>
        </Box>
        <Box
          component="footer"
          sx={{
            py: 3,
            px: 2,
            mt: "auto",
            backgroundColor: (theme) =>
              theme.palette.mode === "light"
                ? theme.palette.grey[200]
                : theme.palette.grey[800],
          }}
        >
          <Container maxWidth="sm">
            <Typography variant="body2" color="text.secondary" align="center">
              © {new Date().getFullYear()} {t("app.name")}
            </Typography>
          </Container>
        </Box>
      </Box>
    </Box>
  );
};

export default Layout;
