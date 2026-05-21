import { useSettingsStore } from '../../store/settingsStore'
import { Switch } from '../ui/Switch'
import { Label } from '../ui/Label'
import { Tooltip } from '../ui/Tooltip'

export function SyncToggle() {
  const { syncEnabled, setSyncEnabled } = useSettingsStore()
  
  return (
    <div className="flex items-center space-x-2">
      <Tooltip content={syncEnabled ? "Cloud sync is enabled" : "Local storage only"}>
        <div className="flex items-center">
          <Label htmlFor="sync-toggle" className="mr-2">Sync to Cloud</Label>
          <Switch
            id="sync-toggle"
            checked={syncEnabled}
            onCheckedChange={setSyncEnabled}
          />
        </div>
      </Tooltip>
    </div>
  )
}