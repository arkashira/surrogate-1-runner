package auth

import (
	"context"
	"time"
)

type LicenseAuditLog struct {
	ID        string
	LicenseID string
	Action    string
	Timestamp int64
	UserID    string
}

type LicenseAuditLogService struct {
	mu           sync.RWMutex
	auditLogs    []LicenseAuditLog
}

func NewLicenseAuditLogService() *LicenseAuditLogService {
	return &LicenseAuditLogService{
		auditLogs: make([]LicenseAuditLog, 0),
	}
}

func (las *LicenseAuditLogService) LogAction(ctx context.Context, licenseID string, action string, userID string) error {
	las.mu.Lock()
	defer las.mu.Unlock()

	logEntry := LicenseAuditLog{
		ID:        uuid.New().String(),
		LicenseID: licenseID,
		Action:    action,
		Timestamp: time.Now().Unix(),
		UserID:    userID,
	}

	las.auditLogs = append(las.auditLogs, logEntry)

	return nil
}

func (las *LicenseAuditLogService) GetAuditLogs(ctx context.Context) ([]LicenseAuditLog, error) {
	las.mu.RLock()
	defer las.mu.RUnlock()

	return las.auditLogs, nil
}