import React from "react";
import { Box, Container, Typography } from "@mui/material";
import { useTranslation } from "react-i18next";
import { Button } from "../components/common/Button";
import { useNavigate } from "react-router-dom";

const NotFound: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "100vh",
          textAlign: "center",
        }}
      >
        <Typography variant="h1" component="h1" gutterBottom>
          404
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom>
          {t("notFound.title")}
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          {t("notFound.description")}
        </Typography>
        <Button onClick={() => navigate("/")}>{t("notFound.backHome")}</Button>
      </Box>
    </Container>
  );
};

export default NotFound;
