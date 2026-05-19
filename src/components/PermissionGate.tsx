import React, { ReactNode, useContext } from 'react';
import { UserContext } from '../contexts/UserContext';
import { useWarehouseRBAC } from '../hooks/useWarehouseRBAC';

interface PermissionGateProps {
  warehouseId: string;                 // Needed for per‑warehouse check
  requiredRoles: string | string[];     // Roles that grant access
  children: ReactNode;
  fallback?: ReactNode;                // Optional fallback UI
}

export const PermissionGate: React.FC<PermissionGateProps> = ({
  warehouseId,
  requiredRoles,
  children,
  fallback = null,
}) => {
  const { user } = useContext(UserContext);
  const { canEdit, loading } = useWarehouseRBAC(warehouseId);

  if (loading) return null; // or a spinner

  if (!user) return fallback; // no user – deny

  const roles = Array.isArray(requiredRoles) ? requiredRoles : [requiredRoles];
  const hasRole = roles.some((role) => user.roles.includes(role));

  if (!hasRole || !canEdit) return fallback;

  return <>{children}</>;
};