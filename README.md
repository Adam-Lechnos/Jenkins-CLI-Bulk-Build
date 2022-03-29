# Jenkins-CLI-Bulk-Build
Perform a rapid series of Jenkins build against its API using a JSON specified list of objects with parameters. Each object may be a different build. By default the tool accesses the prod Jenkins API.

#### Intended Audience
* Developers
* Devops

#### Pre-requisites
* Python 3.7
* Local `build.json` file with list of build objects
* Local `jenkins_token` file with Jenkins API token
 
##### Jenkins Access Token
* Acquire a Jenkins Access Token by logging into Jenkins, selecting your username in the top right hand corner -> 'Configure' -> 'Add new Token'
* For prod Jenkins, save the token within the same directory as the script, inside a filename, `jenkins_token`
  *  For dev, name the file `jenkins_token_dev`
 
##### Build JSON
 * Create a `build.json` file with a list of nested objects. Name each object a custom build name, i.e., `build1` 
 * Specfiy the following nested paramters for each object:
   * "git_repo_url": "`git@github.factset.com:market-data-cloud/*repo name*`" ,
   * "git_release": "`v + git repo release`",
   * "account_name": "`AWS account name`",
   * "aws_region": "`AWS region`",
   * "build_type": "`deploy or destroy`",
   * "json_selector": "`list of JSONs or empty for all`" (optional and defaults to all)
   * "devops_release": "`v + devops code release version`" (optional and defaults to latest unless [iac.json](https://github.factset.com/market-data-cloud/FDSCexample_asg.img#select-devops-release-optional) specified)
     * **note:** for repos which contain an [iac.json](https://github.factset.com/market-data-cloud/FDSCexample_asg.img#select-devops-release-optional), the value specified inside the file will take precedence over the specified release.
   * "regression_tests": "`execute regression test post build for the cloud_resource within the role.json file`" (optional, defaults to 'No')
 
 ##### Example
 ```
 {
    "build1": {
        "git_repo_url": "git@github.com:org/repo.git" ,
        "git_release": "1.0.0",
        "account_name": "aws-account-dev",
        "aws_region": "us-east-1",
    },
    "build2": {
        "git_repo_url": "git@github.com:org/repo.git" ,
        "git_release": "1.0.1",
        "account_name": "aws-account-qa",
        "aws_region": "us-east-1",
    }
}
 ```

#### Usage

##### Help
`jenkins-cli-bulk-build.py -h` [`--help`]

##### Options

* -h, --help
  * show this help message and exit
* -e ENVIRONMENT, --environment ENVIRONMENT
  * Optional. Set the Jenkins envrionment (Prod|Dev, Default=Prod)
* -j JOB, --job JOB
  * Optional. Set the Jenkins job name (Default=api_processor)

##### Examples

  * Perform a series of builds as specified within the `build.json` against prod Jenkins and the default API controller
    * `jenkins-cli-builk-build.py`
  * Perform a series of builds as specified within the `build.json` against dev Jenkins and the default API controller
    * `jenkins-cli-builk-build.py -e dev`
      *  `jenkins_token_dev` with the correct API token specified
  * Perform a series of builds as specified within the `build.json` against dev Jenkins and a non-default controller
    * `jenkins-cli-builk-build.py -e dev -j Test_Controller`
