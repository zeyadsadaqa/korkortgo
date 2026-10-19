import XCTest

/// Runs only against the explicitly built -PreferenceProof app. Never approves a release.
@MainActor final class NativeRouteTests: XCTestCase {
    private var app: XCUIApplication!
    override func setUp() { continueAfterFailure = false; app = XCUIApplication() }
    private func launch(_ mode: String, _ code: String = "S1", scale: String = "1", dark: Bool = false) {
        app.launchEnvironment = ["PROOF_MODE": mode, "PROOF_CODE": code, "PROOF_FONT_SCALE": scale, "PROOF_DARK": dark ? "true" : "false"]
        app.launch()
        XCTAssertTrue(app.wait(for: .runningForeground, timeout: 15))
        XCTAssertFalse(app.staticTexts["Study tools for your driving licence"].exists, "Use the verification framework, not production App")
    }
    private func button(_ label: String) -> XCUIElement { app.buttons.matching(NSPredicate(format: "label == %@", label)).firstMatch }
    private func reach(_ element: XCUIElement, up: Bool = true) {
        let viewport = CGRect(x: app.frame.minX, y: app.frame.minY + 65, width: app.frame.width, height: app.frame.height - 100)
        for _ in 0..<60 {
            if element.exists && element.isHittable && viewport.contains(element.frame) {
                var previous = element.frame
                var stable = 0
                for _ in 0..<30 {
                    RunLoop.current.run(until: Date().addingTimeInterval(0.1))
                    let current = element.frame
                    stable = abs(current.minY - previous.minY) < 1 && abs(current.height - previous.height) < 1 ? stable + 1 : 0
                    previous = current
                    if stable >= 3 && element.isHittable && viewport.contains(current) { return }
                }
            }
            // Slow, held drags avoid fling overshoot. If a large image carries the
            // target above the viewport, reverse rather than repeatedly scrolling away.
            let forward = element.exists ? element.frame.midY >= viewport.midY : up
            let start = app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: forward ? 0.72 : 0.32))
            let end = app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: forward ? 0.32 : 0.72))
            start.press(forDuration: 0.1, thenDragTo: end, withVelocity: .slow, thenHoldForDuration: 0.3)
        }
        record("unreachable-control")
        XCTFail("Native route element was unreachable: \(element)")
    }
    private func record(_ name: String) {
        let tree = XCTAttachment(string: app.debugDescription); tree.name = name + "-tree"; tree.lifetime = .keepAlways; add(tree)
        let image = XCTAttachment(screenshot: app.screenshot()); image.name = name; image.lifetime = .keepAlways; add(image)
    }
    func testLibrarySearchAndSourceReturn() throws {
        launch("learning")
        let input = app.descendants(matching: .any).matching(NSPredicate(format: "label == %@ AND (elementType == %d OR elementType == %d)", "Search lessons", XCUIElement.ElementType.textField.rawValue, XCUIElement.ElementType.textView.rawValue)).firstMatch
        XCTAssertTrue(input.waitForExistence(timeout: 10), "Search must have its persistent native label")
        input.tap(); input.typeText("Your route into driving\n")
        let lesson = app.buttons.matching(NSPredicate(format: "label CONTAINS %@", "Your route into driving")).firstMatch
        reach(lesson); lesson.tap()
        XCTAssertTrue(button("Learning library").waitForExistence(timeout: 10)); record("reader-opening")
        let source = button("Transportstyrelsen: category B"); reach(source); source.tap()
        XCTAssertTrue(button("Back to Sources").waitForExistence(timeout: 10)); record("source-detail")
        let reading = button("Return to reading"); reach(reading); reading.tap()
        XCTAssertTrue(source.waitForExistence(timeout: 10)); XCTAssertTrue(source.isHittable); record("source-return")
        let library = button("Learning library"); reach(library, up: false); library.tap()
        XCTAssertTrue(input.waitForExistence(timeout: 10)); XCTAssertEqual(input.value as? String, "Your route into driving"); record("library-query-return")
        try app.performAccessibilityAudit(for: [.sufficientElementDescription, .trait])
    }
    func testExactReferenceModalAndCatalogueBack() throws {
        launch("learning-sign", "B1", scale: "1.6")
        let enlarge = button("Enlarge image"); reach(enlarge); enlarge.tap()
        XCTAssertTrue(button("Close").waitForExistence(timeout: 10)); record("reference-modal")
        button("Zoom in").tap()
        XCTAssertTrue(app.descendants(matching: .any).matching(NSPredicate(format: "label CONTAINS %@", "150%")).firstMatch.waitForExistence(timeout: 5))
        button("Reset").tap(); button("Close").tap()
        XCTAssertTrue(enlarge.waitForExistence(timeout: 10)); XCTAssertTrue(enlarge.isHittable)
        let back = button("‹ Road signs and reference"); reach(back, up: false); back.tap()
        XCTAssertTrue(button("Learning library").waitForExistence(timeout: 10))
        XCTAssertFalse(app.textFields.firstMatch.exists); XCTAssertFalse(app.textViews.firstMatch.exists); record("reference-catalogue-return")
        try app.performAccessibilityAudit(for: [.sufficientElementDescription, .trait])
    }
    func testUnknownQuestionAndLegacyChooser() throws {
        launch("learning-question", "unknown-question")
        XCTAssertTrue(app.descendants(matching: .any)["Content unavailable"].waitForExistence(timeout: 10)); record("unavailable")
        button("Open learning library").tap(); XCTAssertTrue(button("Sources").waitForExistence(timeout: 10))
        launch("learning-chapter", "The foundations")
        XCTAssertTrue(app.descendants(matching: .any)["Choose related teaching"].waitForExistence(timeout: 10)); record("legacy-chooser")
        let choice = app.buttons.matching(NSPredicate(format: "label != %@", "Open learning library")).firstMatch
        choice.tap(); XCTAssertTrue(button("Learning library").waitForExistence(timeout: 10)); record("chooser-reading")
    }
    func testDeliberateAnswerAndNextReading() throws {
        launch("learning", "M01-L01", scale: "1.6")
        let answer = app.descendants(matching: .any).matching(NSPredicate(format: "label CONTAINS %@", "The amendment has transitional rules")).firstMatch
        let show = button("Show answer"); reach(show)
        XCTAssertFalse(answer.exists); record("answer-hidden"); show.tap()
        XCTAssertTrue(button("Hide answer").waitForExistence(timeout: 5))
        reach(answer); XCTAssertTrue(answer.exists); record("answer-revealed")
        let hide = button("Hide answer"); reach(hide, up: false); hide.tap(); XCTAssertFalse(answer.exists)
        let next = button("Next: Am I ready today?"); reach(next); next.tap()
        XCTAssertTrue(app.descendants(matching: .any)["Am I ready today?"].waitForExistence(timeout: 5)); record("reading-next")
        try app.performAccessibilityAudit(for: [.sufficientElementDescription, .trait])
    }
    func testPendingCandidateSelectionAndNeutralModal() throws {
        launch("candidate", "sign-recognise-A1")
        let description = "Orange black-bordered rectangle with two upward black arrows; the left bends right, with a dashed lower divider and black diagonal wedge at upper left."
        let radio = button(description); reach(radio); radio.tap(); XCTAssertTrue(radio.isSelected)
        let enlarge = button("Enlarge option A image"); reach(enlarge); enlarge.tap()
        XCTAssertTrue(button("Close").waitForExistence(timeout: 5)); record("candidate-neutral-modal")
        XCTAssertFalse(app.staticTexts["Correct answer"].exists)
        button("Zoom in").tap(); button("Reset").tap(); button("Close").tap()
        XCTAssertTrue(radio.waitForExistence(timeout: 5)); XCTAssertTrue(radio.isSelected); record("candidate-pending-return")
        try app.performAccessibilityAudit(for: [.sufficientElementDescription, .trait])
    }

    func testFaintArtworkDeliveryMatrix() throws {
        let codes = ["S5", "S6", "S7", "S11", "S12", "S13", "T1", "T2", "T6", "T8", "T22", "X8"]
        for dark in [false, true] { for scale in ["1", "1.6"] { for code in codes {
            launch("delivery", code, scale: scale, dark: dark)
            let enlarge = button("Enlarge image")
            XCTAssertTrue(enlarge.waitForExistence(timeout: 10))
            XCTAssertFalse(app.staticTexts["Image unavailable. Return and try again."].exists)
            let name = "faint-\(code)-\(dark ? "dark" : "light")-\(scale)"
            record(name + "-inline")
            reach(enlarge); record(name + "-option")
            enlarge.tap(); XCTAssertTrue(button("Close").waitForExistence(timeout: 10))
            button("Zoom in").tap()
            XCTAssertTrue(app.descendants(matching: .any).matching(NSPredicate(format: "label CONTAINS %@", "150%")).firstMatch.waitForExistence(timeout: 5))
            record(name + "-zoom")
            button("Reset").tap(); button("Close").tap()
            XCTAssertTrue(enlarge.waitForExistence(timeout: 5)); XCTAssertTrue(enlarge.isHittable)
        } } }
    }
}
