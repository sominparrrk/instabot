import os
from io import open

from tqdm import tqdm
import cv2

def upload_photo(
    self,
    photo,
    caption=None,
    upload_id=None,
    from_video=False,
    options={}
):
    """Upload photo to Instagram

    @param photo       Path to photo file (String)
    @param caption     Media description (String)
    @param upload_id   Unique upload_id (String). When None, then
                       generate automatically
    @param from_video  A flag that signals whether the photo is loaded from
                       the video or by itself (Boolean, DEPRECATED: not used)
    @param options     Object with difference options, e.g.
                       configure_timeout, rename (Dict)
                       Designed to reduce the number of function arguments!
                       This is the simplest request object.

    @return            Object with state of uploading to Instagram (or False)
    """
    self.small_delay()
    result = self.api.upload_photo(
        photo,
        caption,
        upload_id,
        from_video,
        options=options
    )
    if not result:
        self.logger.info("Photo '{}' is not uploaded.".format(photo))
        return False
    self.logger.info("Photo '{}' is uploaded.".format(photo))
    return result


def download_photo(
    self,
    media_id,
    folder="photos",
    filename=None,
    save_description=False
):
    self.small_delay()

    if not os.path.exists(folder):
        os.makedirs(folder)

    if save_description:
        media = self.get_media_info(media_id)[0]
        caption = media["caption"]["text"] if media["caption"] else ""
        username = media["user"]["username"]
        fname = os.path.join(folder, "{}_{}.txt".format(username, media_id))
        with open(fname, encoding="utf8", mode="w") as f:
            f.write(caption)

    try:
        return self.api.download_photo(media_id, filename, False, folder)
    except Exception:
        self.logger.info("Media with `{}` is not downloaded.".format(media_id))
        return False


def download_photos(self, medias, folder, save_description=False):
    broken_items = []

    if not medias:
        self.logger.info("Nothing to downloads.")
        return broken_items

    self.logger.info("Going to download {} medias.".format(len(medias)))

    for media in tqdm(medias):
        if not self.download_photo(
            media, folder, save_description=save_description
        ):
            self.error_delay()
            broken_items = medias[medias.index(media):]
    return broken_items


#추가한 코드
# 매개변수로 미디어들의 리스트, 유저이름, 저장된 폴더 위치를 받는다.
def check_downloaded_photos(self, medias, username, folder):
    # 방금 저장한 medias인지 확인하기 위한 변수
    downloaded = []
    # 삭제한 사진 갯수를 저장하기 위한 변수
    deletecount = 0
    # 매개변수로 받은 folder 내에 있는 모든 파일들의 리스트
    photolist = os.listdir(folder)
    
    # medias 리스트를 반복문으로 돌면서
    for i in range(len(medias)):

        # 사진을 다운로드 할 때 저장하는 이름
        t = username[1:] + "_" + medias[i]
        tjpg = t + ".jpg"

        print(t)

        # 사진의 이름이 photolist 리스트에 있다면 downloaded 리스트 끝에 추가
        if tjpg in photolist:
            downloaded.append(tjpg)
        else:
            # 한 media에 사진이 여러개라면 사진 이름이 다운로드한 사진 뒤에 순번이 붙기 때문에
            # photolist 안에 사진의 이름이 있나 확인하면 안되고
            # photolist 의 요소가 사진 이름 안에 포함되는지 확인해야 한다.
            # photolist 안에 있는 요소안에 사진 이름이 있다면 downloaded 리스트 끝에 추가한다.
            for j in photolist:
                if t in j:
                    downloaded.append(j)
    # 다운로드한 사진들을 반복문으로 돌면서
    for x in range(len(downloaded)):
        # downloaded 리스트에 있는 사진을 창에 띄운다.
        img = cv2.imread(folder + "\\" + downloaded[x], cv2.IMREAD_COLOR)
        cv2.imshow('image', img)
        # 눌린 키가 esc라면 해당 사진을 삭제한다.
        if cv2.waitKey(0) == 27:
            cv2.destroyAllWindows()
            os.remove(folder + "\\" + downloaded[x])
            deletecount += 1
    # 삭제한 사진의 갯수 출력한다.
    self.logger.info("Deleted {} photos.".format(deletecount))
