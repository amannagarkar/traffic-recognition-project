//
//  CameraViewController.swift
//  CV344
//
//  Created by Aman Nagarkar on 2/17/25.
//

import UIKit
import AVFoundation
import Vision
class CameraViewController : UIViewController  {
    var captureSession: AVCaptureSession!
    var previewLayer: AVCaptureVideoPreviewLayer!
    var detectionOverLat: CALayer! = nil
    var requests = [VNRequest]()
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setupCamera()
        setupVision()
    }
    
    
    func setupCamera(){
        captureSession = AVCaptureSession()
        guard let videoCaptureDevice = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .back) else { return }
        let videoInput: AVCaptureDeviceInput
        
        do{
            videoInput = try AVCaptureDeviceInput(device: videoCaptureDevice)
        } catch {
            return
        }
        
        if captureSession.canAddInput(videoInput) {
            captureSession.addInput(videoInput)
        } else{
            return
        }
        
        let videoOutput = AVCaptureVideoDataOutput()
        videoOutput.setSampleBufferDelegate(self, queue: DispatchQueue(label: "videoQueue"))
        if captureSession.canAddOutput(videoOutput){
            captureSession.addOutput(videoOutput)
        }
        
        previewLayer = AVCaptureVideoPreviewLayer(session: captureSession)
        previewLayer.videoGravity = .resizeAspectFill
        previewLayer.frame = view.layer.bounds
        view.layer.addSublayer(previewLayer)
        
        captureSession.startRunning()
    }
    
    
    func setupVision(){
        
    }
}

extension CameraViewController: AVCaptureVideoDataOutputSampleBufferDelegate {
    func captureOutput(_ output: AVCaptureOutput, didOutput sampleBuffer: CMSampleBuffer, from connection: AVCaptureConnection) {
        guard let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else { return }
        let requestHandler = VNImageRequestHandler(cvPixelBuffer: pixelBuffer, options: [:])
        do {
            try requestHandler.perform(requests)
        } catch {
            print(error)
        }
    }
}
