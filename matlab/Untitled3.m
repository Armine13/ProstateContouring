clear all;

%Get list of all files
imDir = '3D_T2';
imScene = getAllFiles(imDir);
N = numel(imScene);
i = 30;
info = dicominfo(imScene{1});

for i = 1:N,
    % I = dicomread(imScene{i});
[I{i}, map] = dicomread(imScene{i});
figure();imagesc(I{i}); colormap(gray);
% info = dicominfo(imScene{i});
% id{i} = info.PatientID;
% acc{i} = info.InstanceNumber;
end


% imagesc(I); colormap(gray);

info = dicominfo(imScene{i});
% Y = dicomread(info);
% figure, imshow(Y);
% imcontrast;