import SwiftUI
import KorkortKit

struct KorkortView: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> UIViewController {
        MainViewControllerKt.MainViewController()
    }
    func updateUIViewController(_ uiViewController: UIViewController, context: Context) {}
}

@main
struct KorkortApp: App {
    var body: some Scene {
        WindowGroup {
            KorkortView().ignoresSafeArea()
        }
    }
}
