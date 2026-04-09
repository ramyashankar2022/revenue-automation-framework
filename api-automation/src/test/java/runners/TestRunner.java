package runners;
 
import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;
import org.junit.runner.RunWith;
 
@RunWith(Cucumber.class)
@CucumberOptions(
    // Path to .feature files
    features = "src/test/resources/features",
 
    // Package where step definitions live
    glue = "steps",
 
    // Output plugins: pretty console + HTML + JSON reports
    plugin = {
        "pretty",
        "html:target/cucumber-reports/report.html",
        "json:target/cucumber-reports/report.json"
    },
 
    // Cleaner console output (no ANSI colour codes)
    monochrome = true
)
public class TestRunner {
    // Entry point — Cucumber picks this up via @RunWith
}