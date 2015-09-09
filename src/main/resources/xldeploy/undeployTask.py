#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from xldeploy.XLDeployClientUtil import XLDeployClientUtil

xldClient = XLDeployClientUtil.createXLDeployClient(xldeployServer, username, password)

deployment = None
if xldClient.deploymentExists(deploymentPackage, environment):
    print "Preparing  undeployment \n"
    deployment = xldClient.deploymentPrepareUndeploy(deploymentPackage,environment)
else:
    print "Application not currently deployed in %s \n" % environment
    sys.exit()

# deploymentProperties + configure orchestrators
# print "DEBUG: Deployment description is now: %s" % deployment
# Validating the deployment
print "Creating an undeployment task \n"
taskId = xldClient.get_deployment_task_id(deployment)

print "Execute task with id: %s" % taskId
taskState = xldClient.invoke_task_and_wait_for_result(taskId, pollingInterval, numberOfPollingTrials, continueIfStepFails, numberOfContinueRetrials)

if taskState in ('DONE','EXECUTED'):
    print "Deployment ended in %s \n" % taskState
    xldClient.archiveTask(taskId)
    sys.exit(0)

# rollbackOnError
if rollbackOnError and taskState in ('FAILED', 'STOPPED'):
    print "Going to rollback \n"
    xldClient.stopTask(taskId)
    rollBackTaskId = xldClient.deploymentRollback(taskId)
    taskState = xldClient.invoke_task_and_wait_for_result(rollBackTaskId, pollingInterval, numberOfPollingTrials, continueIfStepFails, numberOfContinueRetrials)
    xldClient.archiveTask(rollBackTaskId)
    sys.exit(1)
elif taskState in ('FAILED', 'STOPPED'):
    print "Task failed, rollback not enabled. \n"
    xldClient.cancelTask(taskId)
    sys.exit(1)
