package steps;
 
import io.cucumber.java.en.And;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.restassured.response.Response;
 
import java.util.List;
 
import static io.restassured.RestAssured.given;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;
 
public class OpenLibrarySteps {
 
    private Response response;
 
    // -----------------------------------------------------------------------
    // Given
    // -----------------------------------------------------------------------
 
    @Given("I send a GET request to {string}")
    public void iSendAGETRequestTo(String url) {
        response = given()
                .header("Accept", "application/json")
                .log().uri()                         // logs the request URL
            .when()
                .get(url)
            .then()
                .log().status()                      // logs the response status
                .extract()
                .response();
 
        // Print full response body to console for visibility
        System.out.println("\n==================================================");
        System.out.println("REQUEST URL  : " + url);
        System.out.println("STATUS CODE  : " + response.getStatusCode());
        System.out.println("RESPONSE BODY:");
        System.out.println(response.getBody().asPrettyString());
        System.out.println("==================================================\n");
    }
 
    // -----------------------------------------------------------------------
    // Then — status code
    // -----------------------------------------------------------------------
 
    @Then("the response status code should be {int}")
    public void theResponseStatusCodeShouldBe(int expectedStatusCode) {
        int actualStatusCode = response.getStatusCode();
        System.out.println("[ASSERT] Status code → " + actualStatusCode
                + " (expected " + expectedStatusCode + ")");
        assertThat(
            "HTTP status code mismatch",
            actualStatusCode,
            equalTo(expectedStatusCode)
        );
    }
 
    // -----------------------------------------------------------------------
    // And — single string field assertion
    // Usage: And the "personal_name" field should be "Sachi Rautroy"
    // -----------------------------------------------------------------------
 
    @And("the {string} field should be {string}")
    public void theFieldShouldBe(String fieldName, String expectedValue) {
        String actualValue = response.jsonPath().getString(fieldName);
        System.out.println("[ASSERT] Field '" + fieldName + "' → '" + actualValue + "'"
                + " (expected '" + expectedValue + "')");
        assertThat(
            "Field '" + fieldName + "' value mismatch",
            actualValue,
            equalTo(expectedValue)
        );
    }
 
    // -----------------------------------------------------------------------
    // And — array field contains value assertion
    // Usage: And the "alternate_names" array should contain "Yugashrashta Sachi Routray"
    // -----------------------------------------------------------------------
 //test comment
    @And("the {string} array should contain {string}")
    public void theArrayShouldContain(String fieldName, String expectedValue) {
        List<String> actualList = response.jsonPath().getList(fieldName);
        System.out.println("[ASSERT] Array '" + fieldName + "' → " + actualList);
        System.out.println("         Checking it contains: '" + expectedValue + "'");
        assertThat(
            "Array '" + fieldName + "' does not contain '" + expectedValue + "'",
            actualList,
            hasItem(expectedValue)
        );
    }
}