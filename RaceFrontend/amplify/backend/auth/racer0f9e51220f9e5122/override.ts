import { AmplifyAuthCognitoStackTemplate } from '@aws-amplify/cli-extensibility-helper';

export function override(resources: AmplifyAuthCognitoStackTemplate) {
  // const unauthRole = resources.unauthRole;

  // const basePolicies = Array.isArray(unauthRole.policies)
  //   ? unauthRole.policies
  //   : [unauthRole.policies];

  // unauthRole.policies = [

  //   ...basePolicies,
  //   {
  //     policyName: "amplify-permissions-custom-resources",
  //     policyDocument: {
  //       Version: "2012-10-17",
  //       "Statement": [
  //         {
  //           "Effect": "Allow",
  //           "Action": [
  //             "iot:Connect"
  //           ],
  //           "Resource": "*"
  //         },
  //         {
  //           "Effect": "Allow",
  //           "Action": "iot:Receive",
  //           "Resource": "*"
  //         },
  //         {
  //           "Effect": "Allow",
  //           "Action": "iot:Subscribe",
  //           "Resource": [
  //             "*"
  //           ]
  //         },
  //         {
  //           "Effect": "Allow",
  //           "Action": "iot:Publish",
  //           "Resource": [
  //             "*"
  //           ]
  //         }
  //       ]
  //     },
  //   },
  // ];
}
