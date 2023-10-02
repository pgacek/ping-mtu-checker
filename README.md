# AlertManager Fingerprint Analysis
AlertManager sends alerts to designated receivers. Each alert is uniquely identified by a fingerprint, computed from the label set of the alert. 

The purpose of this documentation is to elucidate the behavior of this fingerprint under various scenarios.

### Testing Platform
The testing platform is built using docker-compose and comprises of Prometheus, AlertManager, an Ubuntu instance with the Node Exporter, and a simple HTTP web server.

You can find a sample alert configuration here. An example of the alert message dispatched by the AlertManager is as follows:

```json
{
  "receiver": "webhook",
  "status": "firing",
  "alerts": [
    {
      "status": "firing",
      "labels": {
        "alert_name": "Check_LowDiskSpace",
        "alert_source": "AM",
        "alertname": "Check_LowDiskSpace",
        "device": "overlay",
        "fstype": "overlay",
        "instance": "node-exporter-ubuntu:9100",
        "job": "node-exporter",
        "monitor": "AM-Body-Check",
        "mountpoint": "/",
        "severity": "info"
      },
      "annotations": {
        "description": "Some description",
        "summary": "Some summary"
      },
      "startsAt": "2023-09-21T22:24:30.337Z",
      "endsAt": "0001-01-01T00:00:00Z",
      "generatorURL": "http://c42bcce1cf09:9090/graph?g0.expr=node_filesystem_free_bytes%7Binstance%3D%22node-exporter-ubuntu%3A9100%22%2Cmountpoint%3D%22%2F%22%7D+%2F+1024+%2F+1024+%2F+1024+%3C+49\u0026g0.tab=1",
      "fingerprint": "cfa231e7b7342048"
    }
  ],
  "groupLabels": {
    "job": "node-exporter"
  },
  "commonLabels": {
    "alert_name": "Check_LowDiskSpace",
    "alert_source": "AM",
    "alertname": "Check_LowDiskSpace",
    "device": "overlay",
    "fstype": "overlay",
    "instance": "node-exporter-ubuntu:9100",
    "job": "node-exporter",
    "monitor": "AM-Body-Check",
    "mountpoint": "/",
    "severity": "info"
  },
  "commonAnnotations": {
    "description": "Some description",
    "summary": "Some summary"
  },
  "externalURL": "http://0d1bac71f9ed:9093",
  "version": "4",
  "groupKey": "{}:{job=\"node-exporter\"}",
  "truncatedAlerts": 0
}
```
For our tests, we are primarily interested in the following field: `["alerts"][0]["fingerprint"]` which has the value `cfa231e7b7342048`.

### Test Scenarios
Here are the scenarios that we considered:

1. Restart AlertManager.
2. Deactivate the alert and then re-trigger it.
3. Modify the alert condition here by inverting the operation from < to >.
4. Omit the label {alert_source="AM"}.
5. Reinstate the label {alert_source="AM"}.
6. Introduce a new label {alert_severity=info}.
7. Add an extra label within the query.
8. Modify the alert name.

For the purpose of this documentation, only the fingerprint value will be showcased.

### Test Results
Initial Fingerprint value: `cfa231e7b7342048`

1. `cfa231e7b7342048` - Post restart, the alert was resent per AlertManager's configuration and the fingerprint remained unchanged.
2. `cfa231e7b7342048` - After deactivating the alert and subsequently triggering it again, the fingerprint persisted.
3. `cfa231e7b7342048` - The fingerprint was unaffected even when the alert condition changed.
4. `3ee26834e74508b2` - On removing the label, two alerts were initially triggered - the previous and the new one. Over time, as configured in AlertManager, the older alert was resolved.
5. `cfa231e7b7342048` - Similar to the fourth point, initially, two alerts were active. Eventually, the one without the label was resolved.
6. `fc2506caabeaa7ca` - Introducing a new label altered the fingerprint.
7. `fc2506caabeaa7ca` - Modifying query labels did not have any impact on the alert fingerprint.
8. `01891df5ced80b2d` - Changing the alert name resulted in a different fingerprint.


### Conclusion
The fingerprint is derived from the alert's name and its labels. Modifications to the alert's conditional expressions do not influence its fingerprint.
