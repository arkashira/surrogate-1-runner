import { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { UserContext } from '../contexts/UserContext';

interface RBACResponse {
  canEdit: boolean;
}

export const useWarehouseRBAC = (warehouseId: string) => {
  const { user } = useContext(UserContext);
  const [canEdit, setCanEdit] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    if (!user || !warehouseId) {
      setCanEdit(false);
      setLoading(false);
      return;
    }

    const fetchRBAC = async () => {
      try {
        const { data } = await axios.get<RBACResponse>(`/api/inventory/${warehouseId}/rbac`);
        setCanEdit(data.canEdit);
      } catch (e) {
        console.error(e);
        setCanEdit(false);
      } finally {
        setLoading(false);
      }
    };

    fetchRBAC();
  }, [user, warehouseId]);

  return { canEdit, loading };
};