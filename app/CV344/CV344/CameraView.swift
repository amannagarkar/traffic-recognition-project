//
//  CameraView.swift
//  CV344
//
//  Created by Aman Nagarkar on 2/17/25.
//

import SwiftUI
import UIKit

struct CameraView: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> CameraViewController {
        return CameraViewController()
    }
    
    func updateUIViewController(_ uiViewController: CameraViewController, context: Context) {
        // no update
    }
}
