import React from "react";
import App from "react/App";
import { expect } from "chai";
import { shallow } from "enzyme";

describe("App Tests", () => {
    it("Renders react-router without throwing errors.", () => {
        const app = shallow(<App />);
        expect(app.getElement().props.className).to.equal("core-app-view");
    });
});
