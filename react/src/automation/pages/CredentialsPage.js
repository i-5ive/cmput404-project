import { Selector } from 'testcafe';

export default class CredentialsPage {
    constructor() {
	    this.username = Selector("#username");
		this.password = Selector("#password");
		this.submitButton = Selector(".credentialsPage .btn");
		this.switchAction = Selector(".credentialsSwitchAction");
		this.errorAlert = Selector(".alert-danger");
    }
    
    async testDisablingSubmit(t) {
        // disabled by default due to empty username/password
        await t.expect(this.submitButton.hasAttribute("disabled")).eql(true);

        // valid credentials
        await t.typeText(this.username, "a_valid_username")
            .expect(this.submitButton.hasAttribute("disabled")).eql(true)
            .typeText(this.password, "password")
            .expect(this.submitButton.hasAttribute("disabled")).eql(false);

        // invalid username
        await t.typeText(this.username, "an invalid_username")
            .expect(this.submitButton.hasAttribute("disabled")).eql(true)
            .pressKey('ctrl+a delete')
            .typeText(this.username, "this_is_not_valid".repeat(15))
            .expect(this.submitButton.hasAttribute("disabled")).eql(true)
            .click(this.username)
            .pressKey('ctrl+a delete')
            .typeText(this.username, "this_is_valid")
            .expect(this.submitButton.hasAttribute("disabled")).eql(false)
            .click(this.username);

        // invalid password
        await t.typeText(this.password, "password".repeat(20))
            .expect(this.submitButton.hasAttribute("disabled")).eql(true);
    }
}
