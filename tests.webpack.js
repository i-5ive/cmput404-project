import { configure } from "enzyme";
import Adapter from "enzyme-adapter-react-16";

const tests = require.context("./src/js/test/unit"),
    react = require.context("./src/js/react"),
    services = require.context("./src/js/services");

// This is information for webpack to know where we keep our test files
// src: https://www.toptal.com/react/how-react-components-make-ui-testing-easy
// authour: Swizec Teller
tests.keys().forEach(tests);

// Adds unloaded files from tests to the coverage report
react.keys().forEach(react);
services.keys().forEach(services);

// This code sets up the ability for us to use Enzyme for testing
// src: https://airbnb.io/enzyme/docs/installation/index.html
configure({ adapter: new Adapter() });

// prevent web requests
window.XMLHttpRequest = () => {
    throw Error("ensure you stub axios requests properly.");
};
