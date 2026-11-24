import Vision
import CoreImage
import CoreGraphics
import Foundation
let args = CommandLine.arguments
let ctx = CIContext()
for i in stride(from: 1, to: args.count, by: 2) {
  let inURL = URL(fileURLWithPath: args[i]), outURL = URL(fileURLWithPath: args[i+1])
  let handler = VNImageRequestHandler(url: inURL)
  let req = VNGenerateForegroundInstanceMaskRequest()
  try handler.perform([req])
  guard let obs = req.results?.first else { print("no subject", args[i]); continue }
  let buf = try obs.generateMaskedImage(ofInstances: obs.allInstances, from: handler, croppedToInstancesExtent: true)
  let ci = CIImage(cvPixelBuffer: buf)
  try ctx.writePNGRepresentation(of: ci, to: outURL, format: .RGBA8, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)!)
  print("ok", args[i+1], obs.allInstances.count)
}
