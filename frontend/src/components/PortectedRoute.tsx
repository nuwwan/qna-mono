import React from "react";
import { useAuth } from "../services/auth/AuthProvider";
import { Route, Navigate, RouteProps, Outlet } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";

const ProtectedRoute: React.FC<RouteProps> = (props: RouteProps) => {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    debugger;
    return <Navigate to="/login" replace />;
  }

  return (
    <MainLayout>
      <Outlet />
    </MainLayout>
  );
};

export default ProtectedRoute;
