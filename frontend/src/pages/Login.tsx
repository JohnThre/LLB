import React, { useState } from "react";
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  Container,
} from "@mui/material";
import { useNavigate, useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useAuth } from "../contexts/AuthContext";
import { bauhausColors } from "../theme";

const Login: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useTranslation();
  const { login } = useAuth();

  const from = location.state?.from?.pathname || "/";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      await login(email, password);
      navigate(from, { replace: true });
    } catch (err) {
      setError(t("auth.loginError"));
    }
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        backgroundColor: bauhausColors.gray[50],
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
        "&::before": {
          content: '""',
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "12px",
          background: `linear-gradient(90deg, ${bauhausColors.red} 0%, ${bauhausColors.red} 33%, ${bauhausColors.yellow} 33%, ${bauhausColors.yellow} 66%, ${bauhausColors.blue} 66%, ${bauhausColors.blue} 100%)`,
        },
      }}
    >
      <Container maxWidth="sm">
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          {/* Bauhaus Logo */}
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              mb: 4,
            }}
          >
            <Box
              sx={{
                width: 60,
                height: 60,
                backgroundColor: bauhausColors.red,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                border: `3px solid ${bauhausColors.black}`,
                mr: 2,
              }}
            >
              <Typography
                variant="h4"
                sx={{
                  color: bauhausColors.white,
                  fontWeight: 700,
                }}
              >
                L
              </Typography>
            </Box>
            <Typography
              variant="h2"
              sx={{
                fontWeight: 700,
                letterSpacing: "0.1em",
                color: bauhausColors.black,
              }}
            >
              LLB
            </Typography>
          </Box>

          <Paper
            elevation={0}
            sx={{
              padding: 4,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              width: "100%",
              backgroundColor: bauhausColors.white,
              border: `3px solid ${bauhausColors.black}`,
              boxShadow: `8px 8px 0px ${bauhausColors.gray[200]}`,
              borderRadius: 0,
            }}
          >
            <Typography 
              component="h1" 
              variant="h4"
              sx={{
                fontWeight: 700,
                textTransform: "uppercase",
                letterSpacing: "0.1em",
                color: bauhausColors.black,
                mb: 3,
              }}
            >
              {t("auth.login", "Login")}
            </Typography>

            <Box
              component="form"
              onSubmit={handleSubmit}
              sx={{ width: "100%" }}
            >
              <Box sx={{ mb: 3 }}>
                <Typography
                  variant="body1"
                  sx={{
                    fontWeight: 600,
                    textTransform: "uppercase",
                    letterSpacing: "0.05em",
                    color: bauhausColors.black,
                    mb: 1,
                  }}
                >
                  {t("auth.email", "Email")}
                </Typography>
                <TextField
                  required
                  fullWidth
                  id="email"
                  name="email"
                  autoComplete="email"
                  autoFocus
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  sx={{
                    "& .MuiOutlinedInput-root": {
                      backgroundColor: bauhausColors.gray[50],
                      borderRadius: 0,
                      "& fieldset": {
                        borderWidth: "2px",
                        borderColor: bauhausColors.black,
                      },
                      "&:hover fieldset": {
                        borderColor: bauhausColors.blue,
                      },
                      "&.Mui-focused fieldset": {
                        borderColor: bauhausColors.red,
                      },
                    },
                  }}
                />
              </Box>

              <Box sx={{ mb: 3 }}>
                <Typography
                  variant="body1"
                  sx={{
                    fontWeight: 600,
                    textTransform: "uppercase",
                    letterSpacing: "0.05em",
                    color: bauhausColors.black,
                    mb: 1,
                  }}
                >
                  {t("auth.password", "Password")}
                </Typography>
                <TextField
                  required
                  fullWidth
                  name="password"
                  type="password"
                  id="password"
                  autoComplete="current-password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  sx={{
                    "& .MuiOutlinedInput-root": {
                      backgroundColor: bauhausColors.gray[50],
                      borderRadius: 0,
                      "& fieldset": {
                        borderWidth: "2px",
                        borderColor: bauhausColors.black,
                      },
                      "&:hover fieldset": {
                        borderColor: bauhausColors.blue,
                      },
                      "&.Mui-focused fieldset": {
                        borderColor: bauhausColors.red,
                      },
                    },
                  }}
                />
              </Box>

              {error && (
                <Box
                  sx={{
                    p: 2,
                    mb: 3,
                    backgroundColor: bauhausColors.red,
                    color: bauhausColors.white,
                    border: `2px solid ${bauhausColors.black}`,
                  }}
                >
                  <Typography
                    sx={{
                      fontWeight: 600,
                      textTransform: "uppercase",
                      letterSpacing: "0.05em",
                    }}
                  >
                    {error}
                  </Typography>
                </Box>
              )}

              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{
                  py: 2,
                  backgroundColor: bauhausColors.blue,
                  color: bauhausColors.white,
                  border: `2px solid ${bauhausColors.black}`,
                  borderRadius: 0,
                  fontWeight: 700,
                  textTransform: "uppercase",
                  letterSpacing: "0.1em",
                  fontSize: "1rem",
                  "&:hover": {
                    backgroundColor: bauhausColors.black,
                  },
                }}
              >
                {t("auth.login", "Login")}
              </Button>
            </Box>
          </Paper>

          {/* Geometric decoration */}
          <Box
            sx={{
              display: "flex",
              gap: 2,
              mt: 4,
            }}
          >
            <Box
              sx={{
                width: 40,
                height: 40,
                backgroundColor: bauhausColors.red,
                border: `2px solid ${bauhausColors.black}`,
              }}
            />
            <Box
              sx={{
                width: 40,
                height: 40,
                backgroundColor: bauhausColors.yellow,
                border: `2px solid ${bauhausColors.black}`,
              }}
            />
            <Box
              sx={{
                width: 40,
                height: 40,
                backgroundColor: bauhausColors.blue,
                border: `2px solid ${bauhausColors.black}`,
              }}
            />
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default Login;