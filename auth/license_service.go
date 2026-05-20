package auth

import (
	"context"
	"fmt"
	"sync"

	"github.com/google/uuid"
)

type License struct {
	ID        string
	UserID    string
	Role      string
	CreatedAt int64
	UpdatedAt int64
}

type LicenseService struct {
	mu     sync.RWMutex
	licenses map[string]License
}

func NewLicenseService() *LicenseService {
	return &LicenseService{
		licenses: make(map[string]License),
	}
}

func (ls *LicenseService) CreateLicense(ctx context.Context, userID string, role string) (*License, error) {
	ls.mu.Lock()
	defer ls.mu.Unlock()

	licenseID := uuid.New().String()
	newLicense := License{
		ID:        licenseID,
		UserID:    userID,
		Role:      role,
		CreatedAt: time.Now().Unix(),
		UpdatedAt: time.Now().Unix(),
	}

	ls.licenses[licenseID] = newLicense

	return &newLicense, nil
}

func (ls *LicenseService) GetLicense(ctx context.Context, licenseID string) (*License, error) {
	ls.mu.RLock()
	defer ls.mu.RUnlock()

	license, exists := ls.licenses[licenseID]
	if !exists {
		return nil, fmt.Errorf("license not found")
	}

	return &license, nil
}

func (ls *LicenseService) UpdateLicense(ctx context.Context, licenseID string, role string) (*License, error) {
	ls.mu.Lock()
	defer ls.mu.Unlock()

	license, exists := ls.licenses[licenseID]
	if !exists {
		return nil, fmt.Errorf("license not found")
	}

	license.Role = role
	license.UpdatedAt = time.Now().Unix()

	return &license, nil
}

func (ls *LicenseService) DeleteLicense(ctx context.Context, licenseID string) error {
	ls.mu.Lock()
	defer ls.mu.Unlock()

	_, exists := ls.licenses[licenseID]
	if !exists {
		return fmt.Errorf("license not found")
	}

	delete(ls.licenses, licenseID)

	return nil
}