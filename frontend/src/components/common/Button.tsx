import React from "react";
import {
  Button as MuiButton,
  ButtonProps as MuiButtonProps,
} from "@mui/material";
import { styled } from "@mui/material/styles";
import { bauhausColors } from "../../theme";

interface ButtonProps extends MuiButtonProps {
  variant?: "contained" | "outlined" | "text";
  color?: "primary" | "secondary" | "success" | "error";
  size?: "small" | "medium" | "large";
}

const StyledButton = styled(MuiButton)(({ theme, variant, color }) => ({
  borderRadius: 0,
  textTransform: "uppercase",
  fontWeight: 700,
  letterSpacing: "0.1em",
  border: `2px solid ${bauhausColors.black}`,
  transition: "all 0.15s ease",
  
  "&.MuiButton-contained": {
    boxShadow: "none",
    backgroundColor: color === "secondary" ? bauhausColors.red : bauhausColors.blue,
    color: bauhausColors.white,
    "&:hover": {
      boxShadow: "none",
      backgroundColor: bauhausColors.black,
      transform: "translate(-2px, -2px)",
      boxShadow: `4px 4px 0px ${bauhausColors.gray[300]}`,
    },
    "&:disabled": {
      backgroundColor: bauhausColors.gray[300],
      color: bauhausColors.gray[500],
      border: `2px solid ${bauhausColors.gray[400]}`,
    },
  },
  
  "&.MuiButton-outlined": {
    backgroundColor: "transparent",
    color: color === "secondary" ? bauhausColors.red : bauhausColors.blue,
    borderColor: color === "secondary" ? bauhausColors.red : bauhausColors.blue,
    borderWidth: "2px",
    "&:hover": {
      backgroundColor: color === "secondary" ? bauhausColors.red : bauhausColors.blue,
      color: bauhausColors.white,
      borderWidth: "2px",
      transform: "translate(-2px, -2px)",
      boxShadow: `4px 4px 0px ${bauhausColors.gray[300]}`,
    },
  },
  
  "&.MuiButton-text": {
    backgroundColor: "transparent",
    color: color === "secondary" ? bauhausColors.red : bauhausColors.blue,
    border: "none",
    "&:hover": {
      backgroundColor: bauhausColors.yellow,
      color: bauhausColors.black,
      border: `2px solid ${bauhausColors.black}`,
    },
  },
  
  "&.MuiButton-sizeSmall": {
    padding: "8px 16px",
    fontSize: "0.75rem",
  },
  
  "&.MuiButton-sizeMedium": {
    padding: "12px 24px",
    fontSize: "0.875rem",
  },
  
  "&.MuiButton-sizeLarge": {
    padding: "16px 32px",
    fontSize: "1rem",
  },
}));

const Button = ({
  children,
  variant = "contained",
  color = "primary",
  size = "medium",
  ...props
}: ButtonProps) => {
  return (
    <StyledButton variant={variant} color={color} size={size} {...props}>
      {children}
    </StyledButton>
  );
};

export default Button;
export { Button };