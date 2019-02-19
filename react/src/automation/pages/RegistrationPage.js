import { Selector } from 'testcafe';

import CredentialsPage from "./CredentialsPage";

export default class RegistrationPage extends CredentialsPage {
    constructor() {
        super();
        this.successAlert = Selector(".alert-success");
    }
}
